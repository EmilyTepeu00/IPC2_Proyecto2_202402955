from flask import Blueprint, request, render_template
from ..utils.xml_parser import XMLParser
from ..utils.procesador_planes import ProcesadorPlanes
from ..modelos.lista_enlazada import ListaEnlazada
from ..utils.generador_reportes import GeneradorReportes
from ..utils.generador_xml_salida import GeneradorXMLSalida

#Crear blueprint para las rutas principales
main_bp = Blueprint('main', __name__)

#Instancias globales
parser = XMLParser()
procesador = ProcesadorPlanes()
generador_reportes = GeneradorReportes()
generador_xml = GeneradorXMLSalida()

@main_bp.route('/')
#PAGINA PRINCIPAL DEL SISTEMA
def pagina_inicio():
    try:
        invernaderos = parser.obtener_invernaderos()

        #Calcular estadisticas
        invernaderos_count = invernaderos.tamaño
        drones_count = parser.obtener_drones().tamaño

        planes_count = 0
        for invernadero in invernaderos:
            planes_count += invernadero.planes_riego.tamaño

        return render_template('index.html',
                               invernaderos_count=invernaderos_count,
                               drones_count=drones_count,
                               planes_count=planes_count)

    except Exception as e:
        #Fallback a version simple en caso de error
        return render_template('index.html', 
                               invernaderos_count=0,
                               drones_count=0,
                               planes_count=0)


#RUTA PARA CARGAR ARCHIVOS XML
@main_bp.route('/cargar-xml', methods=['GET', 'POST'])
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
                                    mensaje="XML cargado con exito", 
                                    detalles=f"Se cargaron {parser.obtener_invernaderos().tamaño} invernaderos")
            else:
                return render_template('error.html', mensaje="Error al procesar el archivo XML")
        else:
            return render_template('error.html', mensaje="Formato de archivo invalido. Solo se aceptan .xml")
            
    except Exception as e:
        return render_template('error.html', mensaje=f"Error: {str(e)}")
    

#LISTAR INVERNADEROS CARGADOS
@main_bp.route('/invernaderos')
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
    

#PROBAR PLAN DE RIEGO PARA UN INVERNADERO ESPECIFICO
@main_bp.route('/probar-plan')
@main_bp.route('/probar-plan/<int:invernadero_id>')
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
    

#MOSTRAR ESTADISTICAS DE AGUA Y FERTILIZANTE
@main_bp.route('/estadisticas')
def mostrar_estadisticas():
    try:
        #Estadisticas
        return render_template('en_desarrollo.html', 
                            funcionalidad="Estadisticas de consumo")
    
    except Exception as e:
        return render_template('error.html', mensaje=f"Error: {str(e)}")
    

#PAGINA PRINCIPAL DE GENERACION DE REPORTES
@main_bp.route('/reportes')
def mostrar_reportes():
    try:
        invernaderos = parser.obtener_invernaderos()
        return render_template('reportes.html', invernaderos=invernaderos)
    except Exception as e:
        return render_template('error.html', mensaje=f"Error: {str(e)}")
    

#GENERAR REPORTE PARA UN INVERNADERO
@main_bp.route('/generar-reporte-html/<int:invernadero_id>')
def generar_reporte_html(invernadero_id):
    try:
        invernaderos = parser.obtener_invernaderos()
        
        if invernaderos.tamaño == 0:
            return render_template('error.html', mensaje="No hay invernaderos cargados")
        
        if invernadero_id >= invernaderos.tamaño:
            return render_template('error.html', mensaje="ID de invernadero invalido")
        
        invernadero = invernaderos.obtener(invernadero_id)
        
        if invernadero.planes_riego.tamaño == 0:
            return render_template('error.html', mensaje="No hay planes de riego")
        
        #Procesar plan para obtener instrucciones
        plan = invernadero.planes_riego.obtener(0)
        contenido_plan = plan.obtener(1)
        instrucciones = procesador.procesar_plan(contenido_plan, invernadero)
        
        #Generar reporte HTML
        reporte_html = generador_reportes.generar_reporte_invernadero_html(
            invernadero, plan, instrucciones
        )
        
        #Guardar reporte
        nombre_archivo = f"reporte_{invernadero.nombre.replace(' ', '_')}.html"
        ruta_guardado = generador_reportes.guardar_reporte_html(reporte_html, nombre_archivo)
        
        if ruta_guardado:
            return render_template('exito.html', 
                                mensaje="Reporte HTML generado con exito",
                                detalles=f"Archivo guardado en: {ruta_guardado}")
        else:
            return render_template('error.html', mensaje="Error al guardar el reporte")
            
    except Exception as e:
        return render_template('error.html', mensaje=f"Error generando reporte: {str(e)}")


#GENERAR GRAFICO GRAPHVIZ PARA UN INVERNADERO
@main_bp.route('/generar-grafo/<int:invernadero_id>')
def generar_grafo(invernadero_id):
    try:
        invernaderos = parser.obtener_invernaderos()
        
        if invernaderos.tamaño == 0:
            return render_template('error.html', mensaje="No hay invernaderos cargados")
        
        if invernadero_id >= invernaderos.tamaño:
            return render_template('error.html', mensaje="ID de invernadero invalido")
        
        invernadero = invernaderos.obtener(invernadero_id)
        
        if invernadero.planes_riego.tamaño == 0:
            return render_template('error.html', mensaje="No hay planes de riego")
        
        #Procesar plan para obtener instrucciones
        plan = invernadero.planes_riego.obtener(0)
        contenido_plan = plan.obtener(1)
        instrucciones = procesador.procesar_plan(contenido_plan, invernadero)
        
        #Generar grafico
        ruta_grafo = generador_reportes.generar_grafo_tdas(invernadero, instrucciones)
        
        if ruta_grafo:
            return render_template('exito.html',
                                mensaje="Grafico Graphviz generado con exito",
                                detalles=f"Imagen guardada en: {ruta_grafo}")
        else:
            return render_template('error.html', mensaje="Error al generar el grafico")
            
    except Exception as e:
        return render_template('error.html', mensaje=f"Error generando grafico: {str(e)}")
        

#EXPORTAR TODOS LOS DATOS A XML
@main_bp.route('/exportar-xml')
def exportar_xml():
    try:
        invernaderos = parser.obtener_invernaderos()
        
        if invernaderos.tamaño == 0:
            return render_template('error.html', mensaje="No hay datos para exportar")
        
        #Generar XML completo
        ruta_xml = generador_xml.generar_xml_completo(parser, procesador)
        
        if ruta_xml:
            return render_template('exito.html',
                                mensaje="Archivo XML de salida generado con exito",
                                detalles=f"Archivo guardado en: {ruta_xml}")
        else:
            return render_template('error.html', mensaje="Error al generar XML de salida")
            
    except Exception as e:
        return render_template('error.html', mensaje=f"Error exportando XML: {str(e)}")

#PAGINA DE EXPORTACION
@main_bp.route('/exportar')
def pagina_exportar():
    try:
        invernaderos = parser.obtener_invernaderos()
        return render_template('exportar.html', invernaderos=invernaderos)
        
    except Exception as e:
        return render_template('error.html', mensaje=f"Error: {str(e)}")
    

#PAGINA DE AYUDA DEL SISTEMA
@main_bp.route('/ayuda')
def pagina_ayuda():
    return render_template('ayuda.html')


#PAGINA ACERCA DEL SISTEMA
@main_bp.route('/acerca-de')
def acerca_de():
    return render_template('acerca_de.html')


#SIMULAR ESTADO DE TDAs EN TIEMPO ESPECIFICO
@main_bp.route('/simular-tiempo/<int:invernadero_id>')
def simular_tiempo(invernadero_id):
    try:
        tiempo_str = request.args.get('tiempo', '0')
        
        if not tiempo_str.isdigit():
            return render_template('error.html', mensaje="El tiempo debe ser un numero valido")
        
        tiempo = int(tiempo_str)
        invernaderos = parser.obtener_invernaderos()
        
        if invernaderos.tamaño == 0:
            return render_template('error.html', mensaje="No hay invernaderos cargados")
        
        if invernadero_id >= invernaderos.tamaño:
            return render_template('error.html', mensaje="ID de invernadero invalido")
        
        invernadero = invernaderos.obtener(invernadero_id)
        
        if invernadero.planes_riego.tamaño == 0:
            return render_template('error.html', mensaje="No hay planes de riego")
        
        #Procesar plan completo primero
        plan = invernadero.planes_riego.obtener(0)
        contenido_plan = plan.obtener(1)
        instrucciones = procesador.procesar_plan(contenido_plan, invernadero)
        
        #Verificar que el tiempo esté en el rango
        if tiempo < 0 or tiempo >= instrucciones.tamaño:
            return render_template('error.html', 
                                mensaje=f"Tiempo {tiempo}s fuera de rango. Rango valido: 0-{instrucciones.tamaño-1}s")
        
        #Obtener estado en tiempo especifico
        estado_tiempo = instrucciones.obtener(tiempo)
        segundos = estado_tiempo.obtener(0)
        acciones = estado_tiempo.obtener(1)
        
        #Preparar datos para el template
        acciones_template = ListaEnlazada()
        for accion in acciones:
            accion_info = ListaEnlazada()
            accion_info.agregar_final(accion.obtener(0))  # dron
            accion_info.agregar_final(accion.obtener(1))  # accion
            acciones_template.agregar_final(accion_info)
        
        #Generar grafico para tiempo especifico
        ruta_grafo = generador_reportes.generar_grafo_tiempo_especifico(invernadero, instrucciones, tiempo)
        
        if ruta_grafo:
            #Mover el grafico a static
            import os
            import shutil
            static_path = "app/static/graficos"
            if not os.path.exists(static_path):
                os.makedirs(static_path)
            
            nombre_archivo = f"grafo_tiempo_{tiempo}.png"
            destino = os.path.join(static_path, nombre_archivo)
            shutil.copy2(ruta_grafo, destino)
            
            return render_template('simulacion_tiempo.html',
                                invernadero=invernadero,
                                tiempo=tiempo,
                                tiempo_total=instrucciones.tamaño,
                                acciones=acciones_template,
                                imagen_grafico=f"graficos/{nombre_archivo}")
        else:
            return render_template('error.html', mensaje="Error al generar el grafico")
            
    except Exception as e:
        return render_template('error.html', mensaje=f"Error en la simulacion: {str(e)}")


#PARA SELECCIONAR INVERNADERO Y PLAN 
@main_bp.route('/seleccionar-plan')
def seleccionar_plan():
    try:
        invernaderos = parser.obtener_invernaderos()
        
        #Preparar datos para template
        datos_invernaderos = ListaEnlazada()
        for invernadero in invernaderos:
            invernadero_info = ListaEnlazada()
            invernadero_info.agregar_final(invernadero.nombre)
            invernadero_info.agregar_final(invernadero.numero_hileras)
            invernadero_info.agregar_final(invernadero.plantas_x_hilera)
            
            #Agregar planes
            planes_info = ListaEnlazada()
            for plan_data in invernadero.planes_riego:
                plan_info = ListaEnlazada()
                plan_info.agregar_final(plan_data.obtener(0))  # nombre
                plan_info.agregar_final(plan_data.obtener(1))  # contenido
                planes_info.agregar_final(plan_info)
            
            invernadero_info.agregar_final(planes_info)
            datos_invernaderos.agregar_final(invernadero_info)
        
        return render_template('seleccionar_plan.html', 
                             invernaderos=datos_invernaderos)
        
    except Exception as e:
        return render_template('error.html', mensaje=f"Error: {str(e)}")


#PROCESAR PLAN SELECCIONADO
@main_bp.route('/procesar-plan-seleccionado', methods=['POST'])
def procesar_plan_seleccionado():
    try:
        invernadero_id = int(request.form.get('invernadero_id', 0))
        plan_id = int(request.form.get('plan_id', 0))
        
        invernaderos = parser.obtener_invernaderos()
        
        if invernaderos.tamaño == 0:
            return render_template('error.html', mensaje="No hay invernaderos cargados")
        
        if invernadero_id >= invernaderos.tamaño:
            return render_template('error.html', mensaje="ID de invernadero invalido")
        
        invernadero = invernaderos.obtener(invernadero_id)
        
        if invernadero.planes_riego.tamaño == 0:
            return render_template('error.html', mensaje="No hay planes de riego")
        
        if plan_id >= invernadero.planes_riego.tamaño:
            return render_template('error.html', mensaje="ID de plan invalido")
        
        #Procesar plan especifico
        plan = invernadero.planes_riego.obtener(plan_id)
        nombre_plan = plan.obtener(0)
        contenido_plan = plan.obtener(1)
        
        instrucciones = procesador.procesar_plan(contenido_plan, invernadero)
        tiempo_total = procesador.obtener_tiempo_total()
        
        #Calcular estadisticas
        agua_total = 0
        fertilizante_total = 0
        estadisticas_drones = ListaEnlazada()
        
        for hilera in invernadero.hileras:
            if hilera.dron_asignado:
                dron = hilera.dron_asignado
                agua_total += dron.agua_utilizada
                fertilizante_total += dron.fertilizante_utilizado
                
                #Crear estaisticas por dron
                stats_dron = ListaEnlazada()
                stats_dron.agregar_final(dron.nombre)
                stats_dron.agregar_final(dron.agua_utilizada)
                stats_dron.agregar_final(dron.fertilizante_utilizado)
                stats_dron.agregar_final(hilera.numero)
                estadisticas_drones.agregar_final(stats_dron)
        
        #Preparar instrucciones para template
        instrucciones_template = ListaEnlazada()
        for tiempo_data in instrucciones:
            tiempo_info = ListaEnlazada()
            tiempo_info.agregar_final(tiempo_data.obtener(0))  # segundos
            
            acciones_tiempo = ListaEnlazada()
            instrucciones_tiempo = tiempo_data.obtener(1)
            for instruccion in instrucciones_tiempo:
                accion_info = ListaEnlazada()
                accion_info.agregar_final(instruccion.obtener(0))  # dron
                accion_info.agregar_final(instruccion.obtener(1))  # accion
                acciones_tiempo.agregar_final(accion_info)
            
            tiempo_info.agregar_final(acciones_tiempo)
            instrucciones_template.agregar_final(tiempo_info)
        
        return render_template('resultado_plan.html',
                            invernadero=invernadero,
                            plan_nombre=nombre_plan,
                            tiempo_total=tiempo_total,
                            agua_total=agua_total,
                            fertilizante_total=fertilizante_total,
                            estadisticas_drones=estadisticas_drones,
                            instrucciones=instrucciones_template)
        
    except Exception as e:
        return render_template('error.html', mensaje=f"Error al procesar plan: {str(e)}")
    

#PARA LIMPIAR TODOS LOS DATOS
@main_bp.route('/limpiar-datos', methods=['POST'])
def limpiar_datos():
    try:
        #Limpiar todos los datos
        parser.limpiar_datos()
        
        #Limpiar el procesador
        procesador.instrucciones_tiempo = ListaEnlazada()
        procesador.tiempo_actual = 0
        procesador.plan_actual = ListaEnlazada()
        
        return render_template('exito.html', 
                            mensaje="Todos los datos han sido borrados",
                            detalles="Se eliminaron invernaderos, drones y planes de riego")
        
    except Exception as e:
        return render_template('error.html', mensaje=f"Error al borrar datos: {str(e)}")