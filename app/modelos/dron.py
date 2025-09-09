#CLASE PARA EL DRON REGADOR
from .lista_enlazada import ListaEnlazada

class Dron:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.hilera_asignada = None
        self.posicion_actual = 0
        self.agua_utilizada = 0
        self.fertilizante_utilizado = 0
        self.instrucciones = ListaEnlazada()

    #MOVER EL DRON UNA POSICION ADELANTE
    def mover_adelante(self):
        self.posicion_actual += 1
        instruccion = f"Adelante (H{self.hilera_asignada}P{self.posicion_actual})"
        self.instrucciones.agregar_final(instruccion)
        return instruccion
    
    #MOVER EL DRON UNA POSICION ATRAS
    def mover_atras(self):
        if self.posicion_actual > 0:
            self.posicion_actual -= 1
        instruccion = f"Atras (H{self.hilera_asignada}P{self.posicion_actual})"
        self.instrucciones.agregar_final(instruccion)
        return instruccion

    #REGAR LA PLANTA
    def regar(self, planta):
        self.agua_utilizada += planta.litros_agua
        self.fertilizante_utilizado += planta.gramos_fertilizante
        instruccion = f"Regar (H{self.hilera_asignada}P{self.posicion_actual})"
        self.instrucciones.agregar_final(instruccion)
        return instruccion
    
    #ESPERAR EN SU POSICION ACTUAL
    def esperar(self):
        instruccion = "Esperar"
        self.instrucciones.agregar_final(instruccion)
        return instruccion
    
    #REINICIAR EL DRON A SU ESTADO INICIAL
    def reiniciar(self):
        self.posicion_actual = 0
        self.agua_utilizada = 0
        self.fertilizante_utilizado = 0
        self.instrucciones = ListaEnlazada()

    def __str__(self):
        return f"{self.nombre} (Hilera {self.hilera_asignada}, Posición {self.posicion_actual})"