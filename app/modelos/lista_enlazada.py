#NODO PARA ESTRUCTURAS DE DATOS ENLAZADAS
class Nodo:
    def __init__(self, datos):
        self.datos = datos
        self.siguiente = None 

#LISTA ENLAZADA
class ListaEnlazada:
    def __init__(self):
        self.cabeza = None #Primer nodo
        self.cola = None #Ultimo nodo
        self.tamaño = 0

    #AGREGAR ELEMENTO AL FINAL DE LA LISTA
    def agregar_final(self, datos):
        nuevo_nodo = Nodo(datos)

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo

        self.tamaño += 1

    def agregar_inicio(self, datos):
        nuevo_nodo = Nodo(datos)

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else: 
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo

        self.tamaño += 1

    #ELIMINAR LA PRIMERA OCURRENCIA DEL DATO ESPECIFICADO
    def eliminar(self, datos):
        if self.cabeza is None:
            return False
        
        #Si es el primer elemento
        if self.cabeza.datos == datos:
            self.cabeza = self.cabeza.siguiente
            if self.cabeza is None:
                self.cola = None
            self.tamaño -= 1
            return True
        
        #Buscar el elemento
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.datos == datos:
                actual.siguiente = actual.siguiente.siguiente
                if actual.siguiente is None:
                    self.cola = actual
                self.tamaño -= 1
                return True
            actual = actual.siguiente

        return False
    
    #BUSCAR ELEMENTO EN LA LISTA
    def buscar(self, datos):
        actual = self.cabeza
        indice = 0
        while actual:
            if actual.datos == datos:
                return indice
            actual = actual.siguiente
            indice += 1
        return -1
    
    #OBTENER EL ELEMENTO ESPECIFICADO
    def obtener(self, indice):
        if indice < 0 or indice >= self.tamaño:
            raise IndexError("ERROR: Indice fuera de rango")
        
        actual = self.cabeza
        for _ in range(indice):
            actual = actual.siguiente
        return actual.datos
    
    #ITERADOR PARA RECORRER LA LISTA
    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.datos
            actual = actual.siguiente

    #DEVOLVER TAMAÑO DE LA LISTA
    def __len__(self):
        return self.tamaño
    
    #LISTA REPRESENTADA EN STRING
    def __str__(self):
        if self.cabeza is None:
            return "Lista vacia"
        
        elementos = ""
        actual = self.cabeza
        while actual:
            elementos += str(actual.datos)
            if actual.siguiente:
                elementos += " -> "
            actual = actual.siguiente
        return elementos