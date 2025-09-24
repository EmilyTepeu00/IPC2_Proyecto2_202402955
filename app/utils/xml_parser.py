from lxml import etree
from ..modelos.lista_enlazada import ListaEnlazada
from ..modelos.dron import Dron
from ..modelos.planta import Planta
from ..modelos.hilera import Hilera
from ..modelos.invernadero import Invernadero

#PARA PARSEAR ARCHIVOS XML
class XMLParser:
    def __init__(self):
        self.drones = ListaEnlazada()
        self.invernaderos = ListaEnlazada()

    #CARGAR Y PARSEAR ARCHIVO XML SEGUN LA RUTA
    def cargar_archivo(self, ruta_archivo):
        try:
            arbol = etree.parse(ruta_archivo)
            raiz = arbol.getroot()

            self._parsear_drones(raiz)
            self._parsear_invernaderos(raiz)
            
            if self.invernaderos.tamaño > 0:
                invernadero = self.invernaderos.obtener(0)
                if invernadero.planes_riego.tamaño > 0:
                    plan = invernadero.planes_riego.obtener(0)

            return True
        
        except Exception as e:
            return False
        
    #PARSEAR LISTA DE DRONES DEL XML
    def _parsear_drones(self, raiz):
        lista_drones = raiz.find('listaDrones')
        if lista_drones is not None:
            for dron_xml in lista_drones.findall('dron'):
                id_dron = int(dron_xml.get('id'))
                nombre_dron = dron_xml.get('nombre')
                nuevo_dron = Dron(id_dron, nombre_dron)
                self.drones.agregar_final(nuevo_dron)

    #PARSEAR INVERNADEROS DEL XML
    def _parsear_invernaderos(self, raiz):
        lista_invernaderos = raiz.find('listaInvernaderos')
        if lista_invernaderos is not None:
            for invernadero_xml in lista_invernaderos.findall('invernadero'):
                self._crear_invernadero(invernadero_xml)

    #CREAR INVERNADERO DESDE EL XML
    def _crear_invernadero(self, invernadero_xml):
        nombre = invernadero_xml.get('nombre')
        num_hileras = int(invernadero_xml.find('numeroHileras').text)
        plantas_x_hilera = int(invernadero_xml.find('plantasXhilera').text)

        invernadero = Invernadero(nombre, num_hileras, plantas_x_hilera)

        #Crear hileras vacias
        for i in range(1, num_hileras + 1):
            hilera = Hilera(i, plantas_x_hilera)
            invernadero.agregar_hilera(hilera)

        self._agregar_plantas(invernadero, invernadero_xml)
        self._asignar_drones(invernadero, invernadero_xml)
        self._agregar_planes_riego(invernadero, invernadero_xml)

        self.invernaderos.agregar_final(invernadero)

    #AGREGAR PLANTAS AL INVERNADERO
    def _agregar_plantas(self, invernadero, invernadero_xml):
        lista_plantas = invernadero_xml.find('listaPlantas')
        if lista_plantas is not None:
            plantas_count = 0
            for planta_xml in lista_plantas.findall('planta'):
                try:
                    hilera_num = int(planta_xml.get('hilera'))
                    posicion = int(planta_xml.get('posicion'))
                    litros_agua = float(planta_xml.get('litrosAgua'))
                    gramos_fertilizante = float(planta_xml.get('gramosFertilizante'))
                    nombre_planta = planta_xml.text.strip() if planta_xml.text else ""
                    
                    nueva_planta = Planta(hilera_num, posicion, litros_agua, gramos_fertilizante, nombre_planta)

                    #Buscar la hilera correspondiente y agregar planta
                    hilera_encontrada = None
                    for hilera in invernadero.hileras:
                        if hilera.numero == hilera_num:
                            hilera_encontrada = hilera
                            break
                    
                    if hilera_encontrada:
                        hilera_encontrada.agregar_planta(nueva_planta)
                        plantas_count += 1
                        
                except Exception as e:
                    continue
            
    #ASIGNAR DRONES A HILERAS
    def _asignar_drones(self, invernadero, invernadero_xml):
        asignaciones = invernadero_xml.find('asignacionDrones')
        if asignaciones is not None:
            for asignacion in asignaciones.findall('dron'):
                id_dron = int(asignacion.get('id'))
                num_hilera = int(asignacion.get('hilera'))

                dron_encontrado = None
                for dron in self.drones:
                    if dron.id == id_dron:
                        dron_encontrado = dron
                        break

                if dron_encontrado:
                    hilera_encontrada = None
                    for hilera in invernadero.hileras:
                        if hilera.numero == num_hilera:
                            hilera_encontrada = hilera
                            break
                    
                    if hilera_encontrada:
                        hilera_encontrada.dron_asignado = dron_encontrado
                        dron_encontrado.hilera_asignada = num_hilera
    
    #AGREGAR PLANES DE RIEGO
    def _agregar_planes_riego(self, invernadero, invernadero_xml):
        planes = invernadero_xml.find('planesRiego')
        if planes is not None:
            for plan_xml in planes.findall('plan'):
                nombre_plan = plan_xml.get('nombre')
                contenido_plan = plan_xml.text.strip() if plan_xml.text else ""

                plan_data = ListaEnlazada()
                plan_data.agregar_final(nombre_plan)
                plan_data.agregar_final(contenido_plan)

                invernadero.planes_riego.agregar_final(plan_data)

    #OBTENER LISTA DE DRONES
    def obtener_drones(self):
        return self.drones
    
    #OBTENER LISTA DE INVERNADEROS
    def obtener_invernaderos(self):
        return self.invernaderos