import heapq
import os
import time


class COSTOSEARCH():
    def __init__(self, mapa):
        # Mapeo de costos
        self.COSTS = {
            0: 1,  # Casilla libre
            1: float('inf'),  # Muro (inaccesible)
            2: 1,  # Punto de partida
            3: 20,  # Tráfico medio
            4: 30,  # Tráfico pesado
            5: 1,  # Pasajero (ignorado en el cálculo de movimiento)
            6: 1   # Destino
        }

        #constatnes
        self.REPRESENTACION_INICIO = 2
        self.REPRESENTACION_PASAJERO = 5
        self.REPRESENTACION_OBJETIVO = 6


        # Definición de los movimientos (arriba, abajo, izquierda, derecha)
        self.MOVEMENTS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.DIRECTIONS = ["arriba", "abajo", "izquierda", "derecha"]

        #Inicializar mapa/mundo una  delas 2 pues
        self.mapa = mapa
        self.start = self.encontrar_objeto(self.REPRESENTACION_INICIO)
        self.goal = self.encontrar_objeto(self.REPRESENTACION_PASAJERO)
        




    def encontrar_objeto(self, valor_objeto):
        for y, array in enumerate(self.mapa):
            for x, valor in enumerate(array):
                if valor == valor_objeto:
                    return (y, x)




    def is_valid(self, x, y, grid):
        return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != 1




    def agregar_nodo(self, tree, cor, cont, cost_app, next_dir_name):
            # Si no hay coordenadas, estamos en la raíz, y agregamos directamente
            if not cor:
                tree[0][2].append((cost_app, cont, [], next_dir_name))
                #imprimir_arbol_clasico(tree)
                return tree
            

            # Empezamos desde el primer nivel de profundidad (sin contar la raíz)
            sub_tree = tree[0][2]
            for i, c in enumerate(cor):
                # Encontramos el nodo que corresponde a 'c' 
                #       [A, [K, L, J]] => c es por asi decir el hijo de A que esa en la c-nesima posicion
                #       en este caso si c fuera 2, el hijo seleccionado seria J
                sub_tree = sub_tree[c][2]

                # Si estamos en el último índice de 'cor', agregamos el nuevo nodo, 
                # esto es que ya llegamos a donde queriamos llegar
                if i + 1 == len(cor):
                    sub_tree.append((cost_app, cont, [], next_dir_name))
                    #print(f"\tAgregado nodo: {(cont, [])}")
            
            return tree




    def search_cost(self, grid, start, goal):
            pq = []#la cola de nodos a evular

            #UN NODO ES IGUAL A = COSTO POCISION HIJOS DIRECCION
            tree = [(0, start, [], "start")]
            heapq.heappush(pq, (0, start, [], "start"))
            visited = [start]
            
            while pq:
                current_cost, current_node, cord, dir_name = heapq.heappop(pq)
                x, y = current_node

                if current_node == goal:
                    return tree, cord
                
                indice = 0
                for i, (dx, dy) in enumerate(self.MOVEMENTS):
                    next_x, next_y = x + dx, y + dy

                    if self.is_valid(next_x, next_y, grid):
                        if (next_x, next_y) not in visited: # verificamos que no sea una posicion donde el, nosexd, no haya pasado ya
                            #se arma el nodo
                            new_cost = current_cost + self.COSTS[grid[next_x][next_y]]
                            next_node = (next_x, next_y)
                            next_cord = cord + [indice]
                            next_dir_name = self.DIRECTIONS[i]

                            #se agrega el nodo a la cola de examinacion
                            heapq.heappush(pq, (new_cost, next_node, next_cord, next_dir_name))
                            tree = self.agregar_nodo(tree, cord, next_node , new_cost, next_dir_name)
                           
                            #se verfica si el nodo que se encontro es la meta
                            if next_node == goal:
                                return tree, next_cord

                            #se aniade una pocision para la lista de hijos y se agrega que este nodo ya se visito
                            indice += 1
                            visited.append(next_node)

            return tree, []




    def imprimir_arbol_clasico(self, lista, prefijo="", es_ultimo=True):
        try:
            costo, posicion, hijos, dir_name = lista
        except:
            costo, posicion, hijos, dir_name = lista[0]

        marcador = "└── " if es_ultimo else "├── "
        print(prefijo + marcador + f"{posicion} [Costo: {costo}, direccion {dir_name}]")

        if hijos:
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            for i, hijo in enumerate(hijos):
                self.imprimir_arbol_clasico(hijo, nuevo_prefijo, i == len(hijos) - 1)




    def crear_salida_gui(self, arbol_final, camino_arbol):
        #costo nodo hijos
        nodo = arbol_final[0]
        costo, cord, hijos, dir_name = nodo
        res = []

        hijos = nodo[2]
        for i, c in enumerate(camino_arbol):
            nodo = hijos[c]
            costo, cord, hijos, dir_name  = nodo
            res.append((cord, dir_name))

        return res




    def solucionar(self):
        #encontrar camino hasta el pasajero
        arbol_final, camino_arbol = self.search_cost(self.mapa, self.start, self.goal)

        #encontrar camino desde el pasajero hata el destino
        self.start = self.encontrar_objeto(self.REPRESENTACION_PASAJERO)
        self.goal = self.encontrar_objeto(self.REPRESENTACION_OBJETIVO)
        arbol_final2, camino_arbol2 = self.search_cost(self.mapa, self.start, self.goal)

        #devolver el camino completo
        return self.crear_salida_gui(arbol_final, camino_arbol) + self.crear_salida_gui(arbol_final2, camino_arbol2)



