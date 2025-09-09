from .lista_enlazada import ListaEnlazada

#PILA FIFO
class Pila:
    def __init__(self):
        self.elementos = ListaEnlazada()

    #AGREGAR ELEMENTO A LA CIMA DE LA PILA
    def apilar(self, elemento):
        self.elementos.agregar_inicio(elemento)

    #REMOVER Y DEVOLVER ELEMENTO A LA CIMA
    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("La pila esta vacia")
        
        cima = self.elementos.obtener(0)
        self.elementos.eliminar(cima)
        return cima
    
    #DEVOLVER ELEMENTO A LA CIMA SIN REMOVERLO
    def cima(self):
        if self.esta_vacia():
            raise IndexError("La pila esta vacia")
        
        return self.elementos.obtener(0)
    
    #VERIFICAR SI LA PILA ESTA VACIA
    def esta_vacia(self):
        return len(self.elementos) == 0
    
    #DEVOLVER EL TAMAÑO DE LA PILA
    def tamaño(self):
        return len(self.elementos)
    
    def __len__(self):
        return self.tamaño()
    
    def __str__(self):
        return str(self.elementos)