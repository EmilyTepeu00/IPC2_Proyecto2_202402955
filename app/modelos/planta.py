#CLASE DE PLANTA EN EL INVERNADERO
class Planta:
    def __init__(self, hilera, posicion, litros_agua, gramos_fertilizante, nombre):
        self.hilera = hilera
        self.posicion = posicion
        self.litros_agua = litros_agua
        self.gramos_fertilizante = gramos_fertilizante
        self.nombre = nombre
        self.regada = False

    def __str__(self):
        return f"Planta {self.nombre} (H{self.hilera}-P{self.posicion})"