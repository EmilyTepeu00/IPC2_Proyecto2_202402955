from flask import Blueprint, request, jsonify, render_template
from ..utils.xml_parser import XMLParser
from ..utils.procesador_planes import ProcesadorPlanes
from ..modelos.lista_enlazada import ListaEnlazada

#Crear blueprint para las rutas principales
main_bp = Blueprint('main', __name__)

#Instancias globales
parser = XMLParser()
procesador = ProcesadorPlanes()

@main_bp.route('/')
def pagina_inicio():
    #RENDERIZA template HTML en lugar de texto plano
    return render_template('index.html')


@main_bp.route('/cargar-xml', methods=['POST'])
#RUTA PARA CARGAR ARCHIVOS XML
def cargar_xml():
    #GET: Mostrar formulario HTML
    if request.method == 'GET':
        return render_template('cargar_xml.html')
    
    #POST: Procesar archivo subido
    try:
        if 'archivo' not in request.files:
            return "No se envió archivo", 400
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            return "Nombre de archivo inválido", 400
        
        if archivo and archivo.filename.endswith('.xml'):
            #Guardar archivo temporalmente
            archivo.save('temp.xml')

            #Procesar XML
            if parser.cargar_archivo('temp.xml'):
                return "XML cargado con exito", 200
            else:
                return "Error al procesar XML", 500
            
        return "Formato de archivo invalido", 400
    
    except Exception as e:
        return f"Error: {str(e)}", 500
    

@main_bp.route('/invernaderos')
#LISTAR INVERNADEROS CARGADOS
def listar_invernaderos():
    try:
        invernaderos = parser.obtener_invernaderos()

        #Preparar datos para pasar al template XML
        datos_invernaderos = ListaEnlazada()
        for invernadero in invernaderos:
            datos_invernaderos.agregar_final({
                'nombre': invernadero.nombre,
                'hileras': invernadero.numero_hileras,
                'plantas_x_hilera': invernadero.plantas_x_hilera
            })

        #Pasar datos al template HTML
        return render_template('invernaderos.html', invernaderos=datos_invernaderos)
    
    except Exception as e:
        return f"Error: {str(e)}", 500
    

@main_bp.route('/probar-plan')
#PROBAR PROCESAMIENTO DE PLAN DE RIEGO
def probar_plan():
    try:
        invernaderos = parser.obtener_invernaderos()
        if invernaderos.tamaño == 0:
            return "No hay invernaderos cargados", 400
        
        invernadero = invernaderos.obtener(0)
        if invernadero.planes_riego.tamaño == 0:
            return "No hay planes de riego", 400
        
        #Procesar primer plan
        plan = invernadero.planes_riego.obtener(0)
        nombre_plan = plan.obtener(0)
        contenido_plan = plan.obtener(1)

        instrucciones = procesador.procesar_plan(contenido_plan, invernadero)
        tiempo_total = procesador.obtener_tiempo_total()

        resultado = ListaEnlazada()
        resultado.agregar_final(f"Plan: {nombre_plan}")
        resultado.agregar_final(f"Tiempo total: {tiempo_total} segundos")
        resultado.agregar_final("Instrucciones por tiempo:")

        for tiempo_data in instrucciones:
            segundos = tiempo_data.obtener(0)
            instrucciones_tiempo = tiempo_data.obtener(1)
            
            tiempo_str = f"  Tiempo {segundos}s:"
            resultado.agregar_final(tiempo_str)

            for instruccion in instrucciones_tiempo:
                dron = instruccion.obtener(0)
                accion = instruccion.obtener(1)
                resultado.agregar_final(f"    {dron}: {accion}")

        return str(resultado), 200
    
    except Exception as e:
        return f"Error: {str(e)}", 500