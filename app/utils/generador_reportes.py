from ..modelos.lista_enlazada import ListaEnlazada
import os
import graphviz

#GENERADOR DE REPORTES HTML Y GRAFICOS
class GeneradorReportes:
    
    def __init__(self):
        self.ruta_reportes = "data/salida/reportes"
        self.crear_directorios()
    
    #CREAR DIRECTORIOS SI NO HAY
    def crear_directorios(self):
        if not os.path.exists(self.ruta_reportes):
            os.makedirs(self.ruta_reportes)
    
    #REPORTE HTML COMPLETO DE UN INVERNADERO
    def generar_reporte_invernadero_html(self, invernadero, plan_riego, instrucciones):
        html = ListaEnlazada()
        
        #Encabezado
        html.agregar_final("<!DOCTYPE html>")
        html.agregar_final("<html lang='es'>")
        html.agregar_final("<head>")
        html.agregar_final("<meta charset='UTF-8'>")
        html.agregar_final("<title>Reporte de Riego - {}</title>".format(invernadero.nombre))
        html.agregar_final("<style>")
        html.agregar_final("body { font-family: Arial, sans-serif; margin: 20px; }")
        html.agregar_final(".header { background: #2c3e50; color: white; padding: 20px; }")
        html.agregar_final(".section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }")
        html.agregar_final(".tiempo { background: #f8f9fa; margin: 10px 0; padding: 10px; }")
        html.agregar_final("table { width: 100%; border-collapse: collapse; }")
        html.agregar_final("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }")
        html.agregar_final("th { background: #f2f2f2; }")
        html.agregar_final("</style>")
        html.agregar_final("</head>")
        html.agregar_final("<body>")
        
        #Header del reporte
        html.agregar_final("<div class='header'>")
        html.agregar_final("<h1>Reporte de Sistema de Riego</h1>")
        html.agregar_final("<h2>{}</h2>".format(invernadero.nombre))
        html.agregar_final("</div>")
        
        #Informacion general
        html.agregar_final("<div class='section'>")
        html.agregar_final("<h3>Informacion General</h3>")
        html.agregar_final("<p><strong>Plan de riego:</strong> {}</p>".format(plan_riego.obtener(0)))
        html.agregar_final("<p><strong>Hileras:</strong> {}</p>".format(invernadero.numero_hileras))
        html.agregar_final("<p><strong>Plantas por hilera:</strong> {}</p>".format(invernadero.plantas_x_hilera))
        html.agregar_final("</div>")
        
        #Estadisticas de drones
        html.agregar_final("<div class='section'>")
        html.agregar_final("<h3>Estadisticas de Drones</h3>")
        html.agregar_final("<table>")
        html.agregar_final("<tr><th>Dron</th><th>Hilera</th><th>Agua (L)</th><th>Fertilizante (g)</th></tr>")
        
        for hilera in invernadero.hileras:
            if hilera.dron_asignado:
                dron = hilera.dron_asignado
                html.agregar_final("<tr>")
                html.agregar_final("<td>{}</td>".format(dron.nombre))
                html.agregar_final("<td>Hilera {}</td>".format(hilera.numero))
                html.agregar_final("<td>{}</td>".format(dron.agua_utilizada))
                html.agregar_final("<td>{}</td>".format(dron.fertilizante_utilizado))
                html.agregar_final("</tr>")
        
        html.agregar_final("</table>")
        html.agregar_final("</div>")
        
        #Instrucciones por tiempo
        html.agregar_final("<div class='section'>")
        html.agregar_final("<h3>⏱️ Linea de Tiempo de Instrucciones</h3>")
        
        for tiempo_data in instrucciones:
            segundos = tiempo_data.obtener(0)
            instrucciones_tiempo = tiempo_data.obtener(1)
            
            html.agregar_final("<div class='tiempo'>")
            html.agregar_final("<h4>Tiempo {} segundos:</h4>".format(segundos))
            html.agregar_final("<ul>")
            
            for instruccion in instrucciones_tiempo:
                dron = instruccion.obtener(0)
                accion = instruccion.obtener(1)
                html.agregar_final("<li><strong>{}:</strong> {}</li>".format(dron, accion))
            
            html.agregar_final("</ul>")
            html.agregar_final("</div>")
        
        html.agregar_final("</div>")
        
        html.agregar_final("</body>")
        html.agregar_final("</html>")
        
        return html
    
    #GRAFICO GRAPHVIZ DEL ESTADO DE LOS TDAs
    def generar_grafo_tdas(self, invernadero, instrucciones, tiempo_especifico=None):
        try:
            dot = graphviz.Digraph(comment='Estado TDAs Sistema Riego')
            
            #Configuracion del grafico
            dot.attr(rankdir='TB', size='8,5')
            
            #Nodo principal del sistema
            titulo_sistema = f'Sistema de Riego\n{invernadero.nombre}'
            if tiempo_especifico is not None:
                titulo_sistema += f'\nTiempo: {tiempo_especifico}s'
                
            dot.node('Sistema', titulo_sistema, 
                    shape='box', style='filled', color='lightblue')
            
            #Nodos para cada dron
            for i, hilera in enumerate(invernadero.hileras):
                if hilera.dron_asignado:
                    dron = hilera.dron_asignado
                    dot.node(f'Dron{i}', f'{dron.nombre}\Posicion: H{dron.hilera_asignada}P{dron.posicion_actual}\nAgua: {dron.agua_utilizada}L\nFert: {dron.fertilizante_utilizado}g', 
                            shape='ellipse', style='filled', color='lightgreen')
                    dot.edge('Sistema', f'Dron{i}')
            
            #Nodo para instrucciones
            total_instrucciones = instrucciones.tamaño
            titulo_instrucciones = f'Instrucciones Generadas\nTotal: {total_instrucciones}s'
            if tiempo_especifico is not None:
                titulo_instrucciones += f'\nTiempo actual: {tiempo_especifico}s'
                
            dot.node('Instrucciones', titulo_instrucciones, 
                    shape='box', style='filled', color='lightyellow')
            dot.edge('Sistema', 'Instrucciones')
            
            #Nodo para plantas regadas
            plantas_regadas = 0
            for hilera in invernadero.hileras:
                for planta in hilera.plantas:
                    if planta.regada:
                        plantas_regadas += 1
            
            dot.node('Plantas', f'Plantas Regadas\n{plantas_regadas} de {invernadero.numero_hileras * invernadero.plantas_x_hilera}', 
                    shape='box', style='filled', color='lightcoral')
            dot.edge('Sistema', 'Plantas')
            
            #Guardar grafico
            nombre_archivo = f"grafo_tdas_{tiempo_especifico}" if tiempo_especifico is not None else "grafo_tdas"
            ruta_grafo = os.path.join(self.ruta_reportes, nombre_archivo)
            dot.render(ruta_grafo, format='png', cleanup=True)
            
            return ruta_grafo + '.png'
            
        except Exception as e:
            print(f"Error generando gráfico Graphviz: {e}")
            return None
    
    #GUARDAR EL REPORTE EN UN ARCHIVO
    def guardar_reporte_html(self, contenido_html, nombre_archivo):
        try:
            ruta_archivo = os.path.join(self.ruta_reportes, nombre_archivo)
            
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                for linea in contenido_html:
                    f.write(linea + '\n')
            
            return ruta_archivo
        except Exception as e:
            print(f"Error guardando reporte HTML: {e}")
            return None
    
    #GRAFICO PARA TIEMPO DADO
    def generar_grafo_tiempo_especifico(self, invernadero, instrucciones, tiempo_especifico):
        try:
            dot = graphviz.Digraph(comment=f'Estado TDAs en Tiempo {tiempo_especifico}')
            dot.attr(rankdir='TB', size='8,5')
        
            #Obtener estado en tiempo especifico
            estado_tiempo = instrucciones.obtener(tiempo_especifico)
            segundos = estado_tiempo.obtener(0)
            acciones = estado_tiempo.obtener(1)
        
            #Nodo principal
            titulo = f'Sistema de Riego - {invernadero.nombre}\nTiempo: {tiempo_especifico}s'
            dot.node('Sistema', titulo, shape='box', style='filled', color='lightblue')
        
            #Procesar acciones del tiempo específico
            for accion in acciones:
                dron_nombre = accion.obtener(0)
                accion_texto = accion.obtener(1)
            
                #Encontrar dron
                dron_obj = None
                for hilera in invernadero.hileras:
                    if hilera.dron_asignado and hilera.dron_asignado.nombre == dron_nombre:
                        dron_obj = hilera.dron_asignado
                        break
            
                if dron_obj:
                    color = 'lightgreen' if 'Regar' in accion_texto else 'lightyellow'
                    dot.node(f'Dron_{dron_nombre}', 
                            f'{dron_nombre}\n{accion_texto}\Posicion: H{dron_obj.hilera_asignada}P{dron_obj.posicion_actual}',
                            shape='ellipse', style='filled', color=color)
                    dot.edge('Sistema', f'Dron_{dron_nombre}')
        
            #Estadisticas de plantas regadas
            plantas_regadas = 0
            for hilera in invernadero.hileras:
                for planta in hilera.plantas:
                    if planta.regada:
                        plantas_regadas += 1
        
            dot.node('Plantas', f'Plantas Regadas\n{plantas_regadas}/{invernadero.numero_hileras * invernadero.plantas_x_hilera}', 
                    shape='box', style='filled', color='lightcoral')
            dot.edge('Sistema', 'Plantas')
        
            #Guardar grafico
            nombre_archivo = f"grafo_tiempo_{tiempo_especifico}"
            ruta_grafo = os.path.join(self.ruta_reportes, nombre_archivo)
            dot.render(ruta_grafo, format='png', cleanup=True)
        
            return ruta_grafo + '.png'
        
        except Exception as e:
            print(f"Error generando grafico de tiempo especifico: {e}")
            return None