from .lista_enlazada import ListaEnlazada

#CLASE DE INVERNADERO COMPLETO
class Invernadero:
    def __init__(self, nombre, numero_hileras, plantas_x_hilera):
        self.nombre = nombre
        self.numero_hileras = numero_hileras
        self.plantas_x_hilera = plantas_x_hilera
        self.hileras = ListaEnlazada()
        self.planes_riego = ListaEnlazada()
        self.asignaciones_drones = ListaEnlazada()

    #AGREGAR HILERA AL INVERNADERO
    def agregar_hilera(self, hilera):
        self.hileras.agregar_final(hilera)

    def __str__(self):
        return f"Invernadero {self.nombre} ({self.numero_hileras} hileras, {self.plantas_x_hilera} plantas/hilera)"
