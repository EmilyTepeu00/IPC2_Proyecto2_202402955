from ..modelos.lista_enlazada import ListaEnlazada
from ..modelos.cola import Cola

#PROCESAR PLANES DE RIEGO
class ProcesadorPlanes:
    def __init__(self):
        self.instrucciones_tiempo = ListaEnlazada()
        self.tiempo_actual = 0

    #PROCESAR PLAN DE RIEGO
    def procesar_plan(self, plan_conetnido, invernadero):
        #Limpiar instrucciones previas
        self.instrucciones_tiempo = ListaEnlazada()
        self.tiempo_actual = 0

        #Parsear el plan
        plantas_a_regar = plan_conetnido.split(',')
        coordenadas = ListaEnlazada()

        for planta in plantas_a_regar:
            planta = planta.strip()
            if '-' in planta:
                partes = planta.split('-')
                if len(partes) == 2:
                    try:
                        hilera = int(partes[0][1:]) #Extraer numero de "H1"
                        posicion = int(partes[1][1:]) #Extraer numero de "P2"
                        
                        #Coordenadas
                        coord = ListaEnlazada()
                        coord.agregar_final(hilera)
                        coord.agregar_final(posicion)
                        coordenadas.agregar_final(coord)

                    except ValueError:
                        continue

        #Generar instrucciones
        self._generar_instrucciones(coordenadas, invernadero)
        
        return self.instrucciones_tiempo
    
    #GENERAR INSTRUCCIONES PARA CADA DRON
    def _generar_instrucciones(self, coordenadas, invernadero):
        #Reiniciar drones a posicion inicial
        for hilera in invernadero.hileras:
            if hilera.dron_asignado:
                hilera.dron_asignado.reiniciar()

        #Procesar cada coordenada del plan
        for coord in coordenadas:
            hilera_num = coord.obtener(0)
            posicion = coord.obtener(1)
            self._procesar_coordenada(hilera_num, posicion, invernadero)   

        #Regresar todos los drones al inicio
        self._regresar_drones_al_inicio(invernadero)

    #PROCESAR COORDENADA ESPECIFICA DEL PLAN
    def _procesar_coordenada(self, hilera_num, posicion, invernadero):
        #Buscar la hilera y dron correspondiente
        hilera = None
        for h in invernadero.hileras:
            if h.numero == hilera_num:
                hilera = h
                break

        if not hilera or not hilera.dron_asignado:
            return
        
        dron = hilera.dron_asignado
        planta = hilera.obtener_planta(posicion)

        if not planta:
            return
        
        #Mover dron a la posicion deseada
        while dron.posicion_actual < posicion:
            self._agregar_instruccion_tiempo(dron, dron.mover_adelante())

        #Regar la planta
        self._agregar_instruccion_tiempo(dron, dron.regar(planta))

        #Marcar planta como regada
        planta.regada = True

    #REGRESAR TODOS LOS DRONES AL INICIO DE SU HILERA
    def _regresar_drones_al_inicio(self, invernadero):
        for hilera in invernadero.hileras:
            if hilera.dron_asignado:
                dron = hilera.dron_asignado
                while dron.posicion_actual > 0:
                    self._agregar_instruccion_tiempo(dron, dron.mover_atras())

    #AGREGAR INSTRUCCION EN EL TIEMPO ACTUAL
    def _agregar_instruccion_tiempo(self, dron, instruccion):
        #Buscar si ya existe un registro para este tiempo
        tiempo_existente = None
        for tiempo_data in self.instrucciones_tiempo:
            if tiempo_data.obtener(0) == self.tiempo_actual: #segundos en posicion0
                tiempo_existente = tiempo_data
                break

        if tiempo_existente:
            #tiempo_data: [segundos, instrucciones]
            instrucciones = tiempo_existente.obtener(1)

            #Instruccion: [nombre_dron, accion]
            nueva_instruccion = ListaEnlazada()
            nueva_instruccion.agregar_final(dron.nombre)
            nueva_instruccion.agregar_final(instruccion)

            instrucciones.agregar_final(nueva_instruccion)

        else:
            #Crear nuevo tiempo: [segundos, instrucciones]
            nuevo_tiempo = ListaEnlazada()
            nuevo_tiempo.agregar_final(self.tiempo_actual)

            #Lista de instrucciones para este tiempo
            instrucciones_tiempo = ListaEnlazada()

            #Crear instruccion: [nombre_dron, accion]
            nueva_instruccion = ListaEnlazada()
            nueva_instruccion.agregar_final(dron.nombre)
            nueva_instruccion.agregar_final(instruccion)
            
            instrucciones_tiempo.agregar_final(nueva_instruccion)
            nuevo_tiempo.agregar_final(instrucciones_tiempo)
            
            self.instrucciones_tiempo.agregar_final(nuevo_tiempo)

        self.tiempo_actual += 1

    #OBTENER EL TIEMPO TOTAL DEL PLAN
    def obtener_tiempo_total(self):
        return self.tiempo_actual
    
    #OBTENER TODAS LAS INSTRUCCIONES POR TIEMPO
    def obtener_instrucciones(self):
        return self.instrucciones_tiempo