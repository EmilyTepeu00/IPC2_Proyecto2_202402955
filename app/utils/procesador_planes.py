from ..modelos.lista_enlazada import ListaEnlazada
from ..modelos.cola import Cola

#PROCESAR PLANES DE RIEGO
class ProcesadorPlanes:
    def __init__(self):
        self.instrucciones_tiempo = ListaEnlazada()
        self.tiempo_actual = 0
        self.plan_actual = ListaEnlazada()

    #PROCESAR PLAN DE RIEGO
    def procesar_plan(self, plan_contenido, invernadero):
        self.instrucciones_tiempo = ListaEnlazada()
        self.tiempo_actual = 0
        self.plan_actual = ListaEnlazada()

        #Parsear el plan
        plantas_a_regar = plan_contenido.split(',')
        for planta in plantas_a_regar:
            planta = planta.strip()
            if '-' in planta:
                partes = planta.split('-')
                if len(partes) == 2:
                    try:
                        hilera = int(partes[0][1:])
                        posicion = int(partes[1][1:]) #Extraer numero de "P2"
                        
                        #Coordenadas
                        coord = ListaEnlazada()
                        coord.agregar_final(hilera)
                        coord.agregar_final(posicion)
                        self.plan_actual.agregar_final(coord)
                    except ValueError:
                        continue

        #Reiniciar drones
        for hilera in invernadero.hileras:
            if hilera.dron_asignado:
                hilera.dron_asignado.reiniciar()

        #Procesar cada planta en el orden del plan
        for coord in self.plan_actual:
            hilera_num = coord.obtener(0)
            posicion = coord.obtener(1)
            self._mover_y_regar(hilera_num, posicion, invernadero)

        #Regresar drones al inicio
        self._regresar_drones_al_inicio(invernadero)
        
        return self.instrucciones_tiempo
    
    def _mover_y_regar(self, hilera_num, posicion, invernadero):
        #Encontrar dron de la hilera
        dron_objetivo = None
        hilera_objetivo = None
        
        for hilera in invernadero.hileras:
            if hilera.numero == hilera_num and hilera.dron_asignado:
                dron_objetivo = hilera.dron_asignado
                hilera_objetivo = hilera
                break
        
        if not dron_objetivo:
            return

        planta_objetivo = hilera_objetivo.obtener_planta(posicion)

        if not planta_objetivo:
            return

        #Mover dron a la posicion
        while dron_objetivo.posicion_actual < posicion:
            self._agregar_instruccion_unica(dron_objetivo, dron_objetivo.mover_adelante(), invernadero)
        
        #Solo un dron puede regar a la vez
        self._agregar_instruccion_unica(dron_objetivo, dron_objetivo.regar(planta_objetivo), invernadero)
        
        planta_objetivo.regada = True

    #SOLO UN DRON PUEDE REALIZAR ACCIONES A LA VEZ
    def _agregar_instruccion_unica(self, dron, instruccion, invernadero):
        #Crear nuevo tiempo
        nuevo_tiempo = ListaEnlazada()
        nuevo_tiempo.agregar_final(self.tiempo_actual)
        
        instrucciones_tiempo = ListaEnlazada()
        
        #instruccion del dron activo
        instruccion_dron = ListaEnlazada()
        instruccion_dron.agregar_final(dron.nombre)
        instruccion_dron.agregar_final(instruccion)
        instrucciones_tiempo.agregar_final(instruccion_dron)
        
        #Los otros drones esperan
        for hilera in invernadero.hileras:
            if hilera.dron_asignado and hilera.dron_asignado != dron:
                instruccion_espera = ListaEnlazada()
                instruccion_espera.agregar_final(hilera.dron_asignado.nombre)
                instruccion_espera.agregar_final("Esperar")
                instrucciones_tiempo.agregar_final(instruccion_espera)
        
        nuevo_tiempo.agregar_final(instrucciones_tiempo)
        self.instrucciones_tiempo.agregar_final(nuevo_tiempo)
        self.tiempo_actual += 1

    def _regresar_drones_al_inicio(self, invernadero):
        for hilera in invernadero.hileras:
            if hilera.dron_asignado:
                dron = hilera.dron_asignado
                while dron.posicion_actual > 0:
                    self._agregar_instruccion_unica(dron, dron.mover_atras(), invernadero)

    def obtener_tiempo_total(self):
        return self.tiempo_actual

    def obtener_instrucciones(self):
        return self.instrucciones_tiempo
    
    #OBTENER ESTADO ESPECIFICO EN TIEMPO DADO
    def obtener_estado_en_tiempo(self, tiempo):
        if tiempo < 0 or tiempo >= self.instrucciones_tiempo.tamaño:
            return None
        
        return self.instrucciones_tiempo.obtener(tiempo)
