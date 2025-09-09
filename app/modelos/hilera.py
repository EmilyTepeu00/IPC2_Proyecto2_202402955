from .lista_enlazada import ListaEnlazada

#CLASE DE HILERA DE PLANTAS
class Hilera:
    def __init__(self, numero, cantidad_plantas):
        self.numero = numero
        self.cantidad_plantas = cantidad_plantas
        self.plantas = ListaEnlazada()
        self.dron_asignado = None

    #AGREGAR PLANTA A LA HILERA
    def agregar_planta(self, planta):
        self.plantas.agregar_final(planta)

    #OBTENER PLANTA POR SU POSICION
    def obtener_planta(self, posicion):
        for planta in self.plantas:
            if planta.posicion == posicion:
                return planta
        return None
    
    def __str__(self):
        return f"Hilera {self.numero} ({self.cantidad_plantas} plantas)"