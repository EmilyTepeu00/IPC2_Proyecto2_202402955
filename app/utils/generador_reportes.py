from ..modelos.lista_enlazada import ListaEnlazada

class GeneradorReportes:
    #REPORTE HTML DE UN INVERNADERO
    def generar_reporte_invernadero(self, invernadero, plan_riego, instrucciones):
        html = ListaEnlazada()

        html.agregar_final("<html><head><title>Reporte de Riego</title></head><body>")
        html.agregar_final(f"<h1>Reporte: {invernadero.nombre}</h1>")
        html.agregar_final(f"<h2>Plan: {plan_riego}</h2>")

        #ESTADISTICAS
        html.agregar_final("<h3>Estadisticas</h3>")
        html.agregar_final("<ul>")

        for hilera in invernadero.hileras:
            if hilera.dron_asignado:
                dron = hilera.dron_asignado
                html.agregar_final(f"<li>{dron.nombre}: {dron.agua_utilizada}L agua, {dron.fertilizante_utilizado}g fertilizante</li>")

        html.agregar_final("</ul>")

        #INSTRUCCIONES POR TIEMPO
        html.agregar_final("<h3>Instrucciones por Tiempo</h3>")
        for tiempo_data in instrucciones:
            segundos = tiempo_data.obtener(0)
            html.agregar_final(f"<h4>Tiempo {segundos}s:</h4><ul>")
            
            instrucciones_tiempo = tiempo_data.obtener(1)
            for instruccion in instrucciones_tiempo:
                dron = instruccion.obtener(0)
                accion = instruccion.obtener(1)
                html.agregar_final(f"<li>{dron}: {accion}</li>")
            
            html.agregar_final("</ul>")
        
        html.agregar_final("</body></html>")
        return html
            