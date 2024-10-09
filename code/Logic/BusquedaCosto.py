import heapq
import time


class BusquedaCosto():
    def __init__(self, mapa):
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
        self.passager = self.encontrar_objeto(self.REPRESENTACION_PASAJERO)
        self.goal = self.encontrar_objeto(self.REPRESENTACION_OBJETIVO)

        #DATOS ARBOLES
        self.nodos_expandidos = 0
        self.profunidad_maxima = 0

        # Mapeo de costos
        self.COSTS = {
            0: 1,  # Casilla libre
            1: float('inf'),  # Muro (inaccesible)
            2: 1,  # Punto de partida
            3: 8,  # Tráfico medio
            4: 15,  # Tráfico pesado
            5: 1,  # Pasajero
            6: 1   # Destino
        }

        #DATOS PARA MOSTRAR EL ARBOL GRAFICAMENTE
        self.acarreo_profundidad = 0
        self.acarreo_nodos = []
        self.final_nodos = []



    def encontrar_objeto(self, valor_objeto): #hay que acomodarla (y, x) => (x, y)
        for y, array in enumerate(self.mapa):
            for x, valor in enumerate(array):
                if valor == valor_objeto:
                    return (y, x)



    def is_valid(self, x, y, grid):
        return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != 1



    def agregar_nodo(self, ARBOL, path, next_cost, nodo, picked_up_passenger, next_dir_name):
            # Si no hay coordenadas, estamos en la raíz, y agregamos directamente
            if not path:
                ARBOL[0][2].append((next_cost, nodo, [], picked_up_passenger, next_dir_name))
                #imprimir_arbol_clasico(tree)
                return ARBOL
            

            # Empezamos desde el primer nivel de profundidad (sin contar la raíz)
            sub_tree = ARBOL[0][2]
            for i, c in enumerate(path):
                # Encontramos el nodo que corresponde a 'c' 
                #       [A, [K, L, J]] => c es por asi decir el hijo de A que esa en la c-nesima posicion
                #       en este caso si c fuera 2, el hijo seleccionado seria J
                sub_tree = sub_tree[c][2]

                # Si estamos en el último índice de 'cor', agregamos el nuevo nodo, 
                # esto es que ya llegamos a donde queriamos llegar
                if i + 1 == len(path):
                    sub_tree.append((next_cost, nodo, [], picked_up_passenger, next_dir_name))
            
            return ARBOL



    def search_cost(self, grid, start, goal):
        CP = []#la cola de nodos a evular

        ARBOL = [(0, start, [], False, "start")]
        heapq.heappush(CP, (0, start, [], False, "start"))
        visited = [(start, False)]

        self.nodos_expandidos += 1
        self.profunidad_maxima += 1
        while CP:
            costo_node, current_node, path, picked_up_passenger, dir_name = heapq.heappop(CP)
            x, y = current_node

            

            indice = 0
            for i, (dx, dy) in enumerate(self.MOVEMENTS):
                next_x, next_y = x + dx, y + dy

                if self.is_valid(next_x, next_y, grid):
                    if ((next_x, next_y), picked_up_passenger) not in visited:

                        #se arma el nodo
                        next_node = (next_x, next_y)
                        next_path = path + [indice]
                        next_dir_name = self.DIRECTIONS[i]
                        next_cost = costo_node + self.COSTS[grid[next_x][next_y]]

                        decision = True if next_node == self.passager and not picked_up_passenger else picked_up_passenger

                        heapq.heappush(CP, (next_cost, next_node, next_path, decision, next_dir_name))
                        ARBOL = self.agregar_nodo(ARBOL, path, next_cost, next_node, decision, next_dir_name)
                        visited.append(((next_node), decision))

                        self.nodos_expandidos += 1
                        self.profunidad_maxima = max(self.profunidad_maxima, (len(next_path) + 1))

                        if next_node == goal and picked_up_passenger:
                            return ARBOL, next_path, next_cost
                        
                        indice += 1
                        self.final_nodos.append([next_node, next_dir_name, decision])

        return ARBOL, []



    def imprimir_arbol_clasico(self, lista, prefijo="", es_ultimo=True):
        resultado = []  # Lista para acumular las cadenas generadas
        try:
            costo, nodo, hijos, up, dir_name = lista
        except:
            costo, nodo, hijos, up, dir_name = lista[0]

        marcador = "--> " if es_ultimo else "|-- "
        resultado.append(prefijo + marcador + f"{nodo} [costo: {costo}] [P? {up}] [direccion {dir_name}]")

        if hijos:
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "|   ")
            for i, hijo in enumerate(hijos):
                resultado.append(self.imprimir_arbol_clasico(hijo, nuevo_prefijo, i == len(hijos) - 1))

        return "\n".join(resultado)  # Unir todas las cadenas y devolver



    def crear_salida_gui(self, arbol_final, camino_arbol):
        #costo nodo hijos
        nodo = arbol_final[0]
        costo, cord, hijos, up, dir_name = nodo
        res = []

        hijos = nodo[2]
        for i, c in enumerate(camino_arbol):
            nodo = hijos[c]
            costo, cord, hijos, up, dir_name  = nodo
            res.append((cord, dir_name))

        return res



    def solucionar(self):
        #encontrar camino hasta el pasajero
        tiempo_inicio = time.time()
        arbol_final, camino_arbol, costo_total = self.search_cost(self.mapa, self.start, self.goal)
        tiempo_final = time.time()
        tiempo_computo = tiempo_final - tiempo_inicio  

        #devolver el camino completo
        return {
            "arbol":  self.imprimir_arbol_clasico(arbol_final),
            "paths": self.crear_salida_gui(arbol_final, camino_arbol),
            "costo": costo_total,
            "nodos_explorados": self.nodos_expandidos,
            "profundidad_maxima": self.profunidad_maxima,
            "tiempo_computo": f"{tiempo_computo:6.5f}",
            "nodos_expandidos": self.final_nodos[1:]
        }




"""
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

motor = BusquedaCosto(entrada1)
solucion = motor.solucionar()

# Imprimimos los caminos encontrados
if solucion["paths"]:
    print("Caminos encontrados a los objetivos:")
    # Imprimimos las métricas
    print(f"Costo: {solucion["costo"]}")
    print(f"Nodos explorados: {solucion['nodos_explorados']}")
    print(f"Profundidad máxima del árbol: {solucion['profundidad_maxima']}")
    print(f"Tiempo de cómputo: {solucion['tiempo_computo']} (S)")
    print(f"\nCAMINO:\n{solucion["paths"]}")
    print(f"\n\nARBOL:\n{solucion["arbol"]}")
else:
    print("No se encontraron caminos para todos los objetivos.")
"""
