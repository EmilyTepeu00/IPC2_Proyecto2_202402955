from .lista_enlazada import ListaEnlazada

#COLA FIFO
class Cola:
    def __init__(self):
        self.elementos = ListaEnlazada()

    #AGREGAR ELEMENTO AL FINAL DE LA COLA
    def encolar(self, elemento):
        self.elementos.agregar_final(elemento)

    #REMOVER Y DEVOLVER ELEMENTO AL FRENTE
    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola esta vacia")
        
        frente = self.elementos.obtener(0)
        self.elementos.eliminar(frente)
        return frente
    
    #DEVOLVER ELEMENTO AL FRENTE SIN REMOVERLO
    def frente(self):
        if self.esta_vacia():
            raise IndexError("La cola esta vacia")
        
        return self.elementos.obtener(0)
    
    #VERIFICAR SI LA COLA ESTA VACIA
    def esta_vacia(self):
        return len(self.elementos) == 0
    
    #DEVOLVER EL TAMAÑO DE LA COLA
    def tamaño(self):
        return len(self.elementos)
    
    def __len__(self):
        return self.tamaño()
    
    def __str__(self):
        return str(self.elementos)
