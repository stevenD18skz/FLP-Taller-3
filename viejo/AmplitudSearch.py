from collections import deque

"""
EN ESTE CASO ESTE ALGORITMO LO QUE HACIA ERA HACER 2 ARBOLES DE BUSQUEDA
PERO ESTO CAMBIO POR LO QUE YA QUEDA OBSOLETO
"""

class BusquedaAmplitud():
    def __init__(self, mapa):
        # Matriz del mapa
        self.REPRESENTACION_INICIO = 2
        self.REPRESENTACION_PASAJERO = 5
        self.REPRESENTACION_OBJETIVO = 6

        # Definición de los movimientos (arriba, abajo, izquierda, derecha)
        self.MOVEMENTS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.DIRECTIONS = ["LEFT", "RIGHT", "UP", "DOWN"]

        #Inicializar mapa/mundo una  delas 2 pues
        self.mapa = mapa
        self.start = self.encontrar_objeto(self.REPRESENTACION_INICIO)
        self.goal = self.encontrar_objeto(self.REPRESENTACION_PASAJERO)





    def encontrar_objeto(self, valor_objeto):
        for y, array in enumerate(self.mapa):
            for x, valor in enumerate(array):
                if valor == valor_objeto:
                    return (x, y)
                




    # Función para verificar si una celda es válida
    def is_valid(self, x, y, nodos_visitados):
        return 0 <= y < len(self.mapa) and 0 <= x < len(self.mapa[0]) and self.mapa[y][x] != 1 and (x, y) not in nodos_visitados





    # BFS modificado para imprimir el árbol y encontrar la ruta
    def crear_arbol_bfs(self, start, target):
        queue = deque([start]) #los nodos que se van a epxandri
        nodos_visitados = set([start])
        arbol = {start: None}  # Diccionario para guardar el árbol de padres
        steps = 0
        
        while queue:
            size = len(queue)

            for _ in range(size):
                x, y = queue.popleft()
                
                # Si hemos alcanzado el objetivo
                if (x, y) == target:
                    return steps, (x, y), arbol
                
                # Explorar en las 4 direcciones
                for i, (direction_x, direction_y) in enumerate(self.MOVEMENTS):
                    eje_x, eje_y = x + direction_x, y + direction_y

                    if self.is_valid(eje_x, eje_y, nodos_visitados):
                        queue.append((eje_x, eje_y)) #nuevo nodo a expandir
                        nodos_visitados.add((eje_x, eje_y)) #
                        arbol[(eje_x, eje_y)] = (x, y, self.DIRECTIONS[i])  #gsuardar el padre y la dirección de este nodo

            steps += 1

        return -1, (-1, -1), arbol  # No se encontró el objetivo





    # Función para reconstruir la ruta desde el inicio hasta un nodo dado con direcciones
    def construis_camino_final(self, arbol_bfs, end):
        camino_pos_direccion = []
        current = end

        while current is not None:
            arbol_bfs_info = arbol_bfs[current]

            if arbol_bfs_info is None:  # Punto de partida
                camino_pos_direccion.append((current, "start"))

            else:
                camino_pos_direccion.append((current, arbol_bfs_info[2]))  # Agregar la dirección

            current = arbol_bfs_info[0:2] if arbol_bfs_info else None  # Moverse al padre

        camino_pos_direccion.reverse()  # Invertir para obtener el camino desde el inicio

        return camino_pos_direccion





    def solucionar(self):
        # paso 1. encontra la ruta desde la posision inicial hasta el pasajero
        pasos_necesarios_pasajero, posicion_del_pasajero, arbol_para_encontrar_pasajero = self.crear_arbol_bfs(self.start, self.goal)
        ruta_pasajero_final = self.construis_camino_final(arbol_para_encontrar_pasajero, posicion_del_pasajero)




        #encontrar camino desde el pasajero hata el destino
        self.start = self.encontrar_objeto(self.REPRESENTACION_PASAJERO)
        self.goal = self.encontrar_objeto(self.REPRESENTACION_OBJETIVO)
        destination_steps, destination_pos, destination_parent = self.crear_arbol_bfs(self.start, self.goal)
        destination_path_with_directions = self.construis_camino_final(destination_parent, destination_pos)


        # paso 3. Ruta completa desde la posisiono inicial hasta le meta final 
        full_path_with_directions = ruta_pasajero_final + destination_path_with_directions[1:]  # Evitar duplicar el punto de partida del destino

        print(f"Nodos del arbol: {len(arbol_para_encontrar_pasajero) + len(destination_parent)}")


        return full_path_with_directions



entrada1 =  [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 0, 0, 0, 4, 0, 0, 0],
    [2, 1, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 3, 3, 0, 4, 0, 0, 0, 4, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 6],
    [5, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
]

motor = BusquedaAmplitud(entrada1)
solucion = motor.solucionar()
print(solucion)

s = {(0, 2): None, 
 (0, 1): (0, 2, 'UP'), 
 (0, 3): (0, 2, 'DOWN'), 
 (0, 0): (0, 1, 'UP'), 
 (1, 3): (0, 3, 'RIGHT'), 
 (0, 4): (0, 3, 'DOWN'), 
 (2, 3): (1, 3, 'RIGHT'), 
 (0, 5): (0, 4, 'DOWN'), 
 (3, 3): (2, 3, 'RIGHT'), 
 (1, 5): (0, 5, 'RIGHT'), 
 (0, 6): (0, 5, 'DOWN'), 
 (4, 3): (3, 3, 'RIGHT'), 
 (3, 2): (3, 3, 'UP'), 
 (3, 4): (3, 3, 'DOWN'), 
 (2, 5): (1, 5, 'RIGHT')}

print(len(s))