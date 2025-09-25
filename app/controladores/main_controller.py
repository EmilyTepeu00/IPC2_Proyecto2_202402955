from flask import Blueprint, request, render_template
from ..utils.xml_parser import XMLParser
from ..utils.procesador_planes import ProcesadorPlanes
from ..modelos.lista_enlazada import ListaEnlazada

#Crear blueprint para las rutas principales
main_bp = Blueprint('main', __name__)

#Instancias globales
parser = XMLParser()
procesador = ProcesadorPlanes()

@main_bp.route('/')
#PAGINA PRINCIPAL DEL SISTEMA
def pagina_inicio():
    return render_template('index.html')


@main_bp.route('/cargar-xml', methods=['GET', 'POST'])
#RUTA PARA CARGAR ARCHIVOS XML
def cargar_xml():
    #GET: Mostrar formulario HTML
    if request.method == 'GET':
        return render_template('cargar_xml.html')
    
    #POST: Procesar archivo subido
    try:
        if 'archivo' not in request.files:
            return render_template('error.html', mensaje="No se envió archivo")
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            return render_template('error.html', mensaje="Nombre de archivo invalido")
        
        if archivo and archivo.filename.endswith('.xml'):
            #Guardar archivo temporalmente
            archivo_path = 'data/entrada/temp.xml'
            archivo.save(archivo_path)
            
            #Procesar XML
            if parser.cargar_archivo(archivo_path):
                return render_template('exito.html', 
                                    mensaje="XML cargado con ecito", 
                                    detalles=f"Se cargaron {parser.obtener_invernaderos().tamaño} invernaderos")
            else:
                return render_template('error.html', mensaje="Error al procesar el archivo XML")
        else:
            return render_template('error.html', mensaje="Formato de archivo invalido. Solo se aceptan .xml")
            
    except Exception as e:
        return render_template('error.html', mensaje=f"Error: {str(e)}")
    

@main_bp.route('/invernaderos')
#LISTAR INVERNADEROS CARGADOS
def listar_invernaderos():
    try:
        invernaderos = parser.obtener_invernaderos()
        
        #Preparar datos para template
        datos_invernaderos = ListaEnlazada()
        for invernadero in invernaderos:
            invernadero_data = ListaEnlazada()
            invernadero_data.agregar_final(invernadero.nombre)
            invernadero_data.agregar_final(invernadero.numero_hileras)
            invernadero_data.agregar_final(invernadero.plantas_x_hilera)
            datos_invernaderos.agregar_final(invernadero_data)
        
        return render_template('invernaderos.html', invernaderos=datos_invernaderos)
    
    except Exception as e:
        return render_template('error.html', mensaje=f"Error al cargar invernaderos: {str(e)}")
    

@main_bp.route('/probar-plan')
@main_bp.route('/probar-plan/<int:invernadero_id>')
#PROBAR PLAN DE RIEGO PARA UN INVERNADERO ESPECIFICO
def probar_plan(invernadero_id=0):
    try:
        invernaderos = parser.obtener_invernaderos()
        
        if invernaderos.tamaño == 0:
            return render_template('error.html', mensaje="No hay invernaderos cargados")
        
        #Validar ID del invernadero
        if invernadero_id >= invernaderos.tamaño:
            return render_template('error.html', mensaje="ID de invernadero invalido")
        
        invernadero = invernaderos.obtener(invernadero_id)
        
        if invernadero.planes_riego.tamaño == 0:
            return render_template('error.html', mensaje="No hay planes de riego para este invernadero")
        
        #Procesar primer plan
        plan = invernadero.planes_riego.obtener(0)
        nombre_plan = plan.obtener(0)
        contenido_plan = plan.obtener(1)
        
        #Generar instrucciones
        instrucciones = procesador.procesar_plan(contenido_plan, invernadero)
        tiempo_total = procesador.obtener_tiempo_total()
        
        #Preparar datos para template
        resultado = {
            'plan': nombre_plan,
            'tiempo_total': tiempo_total,
            'instrucciones': []
        }
        
        #Convertir instrucciones a formato para template
        for tiempo_data in instrucciones:
            segundos = tiempo_data.obtener(0)
            instrucciones_tiempo = tiempo_data.obtener(1)
            
            tiempo_info = {
                'segundos': segundos,
                'acciones': []
            }
            
            for instruccion in instrucciones_tiempo:
                dron = instruccion.obtener(0)
                accion = instruccion.obtener(1)
                tiempo_info['acciones'].append({
                    'dron': dron,
                    'accion': accion
                })
            
            resultado['instrucciones'].append(tiempo_info)
        
        return render_template('probar_plan.html', resultado=resultado)
    
    except Exception as e:
        return render_template('error.html', mensaje=f"Error al procesar plan: {str(e)}")
    

@main_bp.route('/estadisticas')
#MOSTRAR ESTADISTICAS DE AGUA Y FERTILIZANTE
def mostrar_estadisticas():
    try:
        #Estadisticaaaaaaaaas
        return render_template('en_desarrollo.html', 
                            funcionalidad="Estadisticas de consumo")
    
    except Exception as e:
        return render_template('error.html', mensaje=f"Error: {str(e)}")