from collections import deque
from queue import PriorityQueue

class Nodo:
    def __init__(self, estado, padre, movimiento, profundidad, piezas_correctas):        
        self.estado = estado                        # posición atual de las piezas
        self.padre = padre                          # nodo desde el que se llega a este nodo
        self.movimiento = movimiento                # movimiento para encontrar este nodo desde el padre
        self.profundidad = profundidad              # posición del nodo en el árbol de búsqueda
        self.piezas_correctas = piezas_correctas    # total de piezas en su lugar para este estado

    def __lt__(self, other):
        return ((9 - self.piezas_correctas) < (9 - other.piezas_correctas))

    # mover las piezas en direcciones posibles
    def mover(self, direccion):
        estado = list(self.estado)
        indice = estado.index(0)

        if direccion == 'abajo':            
            if indice not in [6, 7, 8]:                
                temp = estado[indice + 3]
                estado[indice + 3] = estado[indice]
                estado[indice] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == 'arriba':            
            if indice not in [0, 1, 2]:                
                temp = estado[indice - 3]
                estado[indice - 3] = estado[indice]
                estado[indice] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == 'izquierda':            
            if indice not in [0, 3, 6]:                
                temp = estado[indice - 1]
                estado[indice - 1] = estado[indice]
                estado[indice] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == 'derecha':            
            if indice not in [2, 5, 8]:                
                temp = estado[indice + 1]
                estado[indice + 1] = estado[indice]
                estado[indice] = temp
                return tuple(estado)
            else:                
                return None        

    def encontrar_sucesores(self, estado_final):
        sucesores = []
        sucesor0 = self.mover('arriba')
        sucesor1 = self.mover('abajo')
        sucesor2 = self.mover('derecha')
        sucesor3 = self.mover('izquierda')
        
        sucesores.append(Nodo(sucesor0, self, 'arriba', self.profundidad + 1, calcular_heurisitica(sucesor0, estado_final)))
        sucesores.append(Nodo(sucesor1, self, 'abajo', self.profundidad + 1, calcular_heurisitica(sucesor1, estado_final)))
        sucesores.append(Nodo(sucesor2, self, 'derecha', self.profundidad + 1, calcular_heurisitica(sucesor2, estado_final)))
        sucesores.append(Nodo(sucesor3, self, 'izquierda', self.profundidad + 1, calcular_heurisitica(sucesor3, estado_final)))
        
        sucesores = [nodo for nodo in sucesores if nodo.estado != None] # descartar los nodos vacíos (que no pueden generarse)
        return sucesores

    # encontrar el camino desde el nodo inicial hasta el actual
    def encontrar_camino(self):
        camino = []
        nodo_actual = self
        while nodo_actual.profundidad >= 1:
            camino.append(nodo_actual)
            nodo_actual = nodo_actual.padre
        camino.reverse()
        return camino

    # imprimir ordenadamente el estado (piezas) de un nodo
    def imprimir_nodo(self):
        renglon = 0
        for pieza in self.estado:
            if pieza == 0:
                print(' ', end = ' ')
            else:
                print (pieza, end = ' ')
            renglon += 1
            if renglon == 3:
                print()
                renglon = 0       

# calcular la cantidad de piezas que están en su lugar para un estado dado
def calcular_heurisitica(estado_inicial, estado_final):
    valor_correcto = 0
    piezas_correctas = 0
    if estado_inicial:
        for valor_pieza, valor_correcto in zip(estado_inicial, estado_final):
            if valor_pieza == valor_correcto:
                piezas_correctas += 1
            valor_correcto += 1
    return piezas_correctas   

# Algoritmo Breadth First Search
def bfs(inicial, meta):
    visitados = set()   #Conjunto de estados visitados para no visitar el mismo estado más de una vez.
    frontera = deque()  #Cola de nodos aún por explorar. Se agrega el nodo inicial.  
    frontera.append(Nodo(inicial, None, None, 0, calcular_heurisitica(inicial, meta)))
    costo_camino = 0
    
    while frontera:                         #Mientras haya nodos por explorar:
        nodo = frontera.popleft()           #Se toma el primer nodo de la cola.

        if nodo.estado not in visitados:    #Si no se había visitado, 
            visitados.add(nodo.estado)      #se agrega al conjunto de visitados.
            costo_camino = costo_camino + 1
            nodo.imprimir_nodo()
            print("")
        else:                               #Si ya se había visitado
            continue                        #se ignora.
        
        if nodo.estado == meta:                         #Si es una meta, 
            print('\nMeta encontrada')            
            return nodo.encontrar_camino(), costo_camino - 1     #se regresa el camino para llegar a él y termina el algoritmo.        
        else:                                           #Si no es una meta, 
            frontera.extend(nodo.encontrar_sucesores(meta)) #se agregan sus sucesores a los nodos por explorar.

# Algoritmo Depth-limited Search


# Algoritmo Iterative deepening depth-first search

# Algoritmo A*


# Algoritmo Best-first Search


if __name__ == '__main__':
    estado_inicial = (1, 4, 3, 7, 0, 6, 5, 8, 2)
    #estado_final = (1, 4, 3, 7, 6, 2, 5, 8, 0)
    # estado_final = (1, 4, 3, 5, 7, 6, 0, 8, 2)
    estado_final = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    limite = 1
    # # -------------------- BFS --------------------

    print('----- BFS -----')
    nodo_inicial = Nodo(estado_inicial, None, None, 0, calcular_heurisitica(estado_inicial, estado_final))
    nodos_camino, costo_camino = bfs(estado_inicial, estado_final)

   
    if nodos_camino:
        print('Nodos expandidos:', costo_camino)
        print('\nEstado inicial:\n')
        nodo_inicial.imprimir_nodo()
        print ('\nPiezas correctas:', calcular_heurisitica(estado_inicial, estado_final), '\n')
        for nodo in nodos_camino:
            print('Siguiente movimiento:', nodo.movimiento)
            print('Estado actual:\n')
            nodo.imprimir_nodo()
            print('\nPiezas correctas:', nodo.piezas_correctas, '\n')
    