from ..modelos.lista_enlazada import ListaEnlazada
import os

#GENERAR ARCHIVOS XML DE SALIDA
class GeneradorXMLSalida:
    
    def __init__(self):
        self.ruta_salida = "data/salida/xml"
        self.crear_directorios()
    
    #CREAR DIRECTORIO DE SALIDA SI NO HAY
    def crear_directorios(self):
        if not os.path.exists(self.ruta_salida):
            os.makedirs(self.ruta_salida)
    
    #GENERACION DEL XML
    def generar_xml_completo(self, parser, procesador):
        try:
            xml_lineas = ListaEnlazada()
            
            #Encabezado
            xml_lineas.agregar_final('<?xml version="1.0"?>')
            xml_lineas.agregar_final('<datosSalida>')
            xml_lineas.agregar_final('<ListaInvernaderos>')
            
            invernaderos = parser.obtener_invernaderos()
            for invernadero in invernaderos:
                self._agregar_invernadero_xml(xml_lineas, invernadero, procesador)
            
            xml_lineas.agregar_final('</ListaInvernaderos>')
            xml_lineas.agregar_final('</datosSalida>')
            
            #Guardar archivo
            ruta_archivo = os.path.join(self.ruta_salida, 'salida.xml')
            self._guardar_xml(xml_lineas, ruta_archivo)
            
            return ruta_archivo
            
        except Exception as e:
            print(f"Error al generar el XML de salida: {e}")
            return None
    
    #AGREGAR DATOS DE UN INVERNADERO AL XML
    def _agregar_invernadero_xml(self, xml_lineas, invernadero, procesador):
        xml_lineas.agregar_final(f'<invernadero nombre=\"{invernadero.nombre}\">')
        xml_lineas.agregar_final('<listaPlanes>')
        
        #Procesar cada plan del invernadero
        for plan_data in invernadero.planes_riego:
            nombre_plan = plan_data.obtener(0)
            contenido_plan = plan_data.obtener(1)
            
            #Procesar plan para obtener estadisticas
            instrucciones = procesador.procesar_plan(contenido_plan, invernadero)
            tiempo_total = procesador.obtener_tiempo_total()
            
            self._agregar_plan_xml(xml_lineas, nombre_plan, invernadero, instrucciones, tiempo_total)
        
        xml_lineas.agregar_final('</listaPlanes>')
        xml_lineas.agregar_final('</invernadero>')
    
    #AGREGAR DATOS DE UN PLAN ESPECIFICO AL XML
    def _agregar_plan_xml(self, xml_lineas, nombre_plan, invernadero, instrucciones, tiempo_total):
        xml_lineas.agregar_final(f'<plan nombre=\"{nombre_plan}\">')
        
        #Calcular estadisticas de agua y fertilizante
        agua_total, fertilizante_total = self._calcular_estadisticas(invernadero)
        
        xml_lineas.agregar_final(f'<tiempoOptimoSegundos>{tiempo_total}</tiempoOptimoSegundos>')
        xml_lineas.agregar_final(f'<aguaRequeridaLitros>{agua_total}</aguaRequeridaLitros>')
        xml_lineas.agregar_final(f'<fertilizanteRequeridoGramos>{fertilizante_total}</fertilizanteRequeridoGramos>')
        
        #Estadisticas por dron
        xml_lineas.agregar_final('<eficienciaDronesRegadores>')
        for hilera in invernadero.hileras:
            if hilera.dron_asignado:
                dron = hilera.dron_asignado
                xml_lineas.agregar_final(f'<dron nombre=\"{dron.nombre}\" litrosAgua=\"{dron.agua_utilizada}\" gramosFertilizante=\"{dron.fertilizante_utilizado}\"/>')
        xml_lineas.agregar_final('</eficienciaDronesRegadores>')
        
        #Instrucciones por tiempo
        xml_lineas.agregar_final('<instrucciones>')
        for tiempo_data in instrucciones:
            segundos = tiempo_data.obtener(0)
            xml_lineas.agregar_final(f'<tiempo segundos=\"{segundos}\">')
            
            instrucciones_tiempo = tiempo_data.obtener(1)
            for instruccion in instrucciones_tiempo:
                dron = instruccion.obtener(0)
                accion = instruccion.obtener(1)
                xml_lineas.agregar_final(f'<dron nombre=\"{dron}\" accione=\"{accion}\"/>')
            
            xml_lineas.agregar_final('</tiempo>')
        xml_lineas.agregar_final('</instrucciones>')
        
        xml_lineas.agregar_final('</plan>')
    
    #CALCULAR ESTADISTICAS TOTALES DE AGUA Y FERTILIZANTE
    def _calcular_estadisticas(self, invernadero):
        agua_total = 0
        fertilizante_total = 0
        
        for hilera in invernadero.hileras:
            if hilera.dron_asignado:
                dron = hilera.dron_asignado
                agua_total += dron.agua_utilizada
                fertilizante_total += dron.fertilizante_utilizado
        
        return agua_total, fertilizante_total
    
    #GUARDAR EL XML EN ARCHIVO
    def _guardar_xml(self, xml_lineas, ruta_archivo):
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                for linea in xml_lineas:
                    f.write(linea + '\n')
            return True
        
        except Exception as e:
            print(f"Error al guardar el XML: {e}")
            return False