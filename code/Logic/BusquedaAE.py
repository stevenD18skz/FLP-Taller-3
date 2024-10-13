import heapq
import time


class BusquedaAE():
    def __init__(self, grid):
        """
        Constructor de la clase CostSearch.

        Parámetros:
        grid (list de listas): El grid (matriz) que representa el mapa del entorno.
        
        Atributos:
        START_REPRESENTATION (int): Representación del punto de inicio en el grid.
        PASSENGER_REPRESENTATION (int): Representación del pasajero en el grid.
        GOAL_REPRESENTATION (int): Representación del punto objetivo en el grid.
        MOVEMENTS (list): Lista de posibles movimientos (arriba, abajo, izquierda, derecha).
        DIRECTIONS (list): Nombres de las direcciones de movimiento.
        grid (list de listas): El grid que almacena el entorno.
        start (tuple): Coordenadas del punto de inicio.
        passenger (tuple): Coordenadas del pasajero.
        goal (tuple): Coordenadas del objetivo.
        explored_nodes (int): Número de nodos explorados.
        max_depth (int): Profundidad máxima alcanzada durante la búsqueda.
        COSTS (dict): Mapa de costos para los diferentes tipos de terreno.
        final_nodes (list): Lista de nodos finales (solución).
        """
        
        # Representación del inicio, pasajero y objetivo en el grid
        self.START_REPRESENTATION = 2
        self.PASSENGER_REPRESENTATION = 5
        self.GOAL_REPRESENTATION = 6

        # Definición de los movimientos posibles (arriba, abajo, izquierda, derecha)
        self.MOVEMENTS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.DIRECTIONS = ["arriba", "abajo", "izquierda", "derecha"]

        # Inicialización del grid
        self.grid = grid
        self.start = self.find_object(self.START_REPRESENTATION)  # Encontrar punto de inicio
        self.passenger = self.find_object(self.PASSENGER_REPRESENTATION)  # Encontrar pasajero
        self.goal = self.find_object(self.GOAL_REPRESENTATION)  # Encontrar objetivo

        # Datos para la búsqueda de nodos
        self.explored_nodes = 0  # Contador de nodos explorados
        self.max_depth = 0  # Profundidad máxima alcanzada

        # Mapa de costos para los diferentes tipos de terreno
        self.COSTS = {
            0: 1,   # Espacio libre
            1: float('inf'),  # Pared (inaccesible)
            2: 1,   # Punto de inicio
            3: 8,   # Tráfico medio
            4: 15,  # Tráfico pesado
            5: 1,   # Pasajero
            6: 1    # Objetivo
        }

        # Datos para la visualización del árbol de búsqueda
        self.final_nodes = []  # Nodos finales (solución)




    def find_object(self, object_value):
        """
        Encuentra la posición de un objeto en el grid.

        Parámetros:
        object_value (int): Valor que representa el objeto en el grid.

        Retorna:
        tuple: Coordenadas (y, x) del objeto encontrado.
        """
        for y, row in enumerate(self.grid):  # Itera sobre las filas del grid
            for x, value in enumerate(row):  # Itera sobre los valores en cada fila
                if value == object_value:  # Si el valor coincide con el objeto buscado
                    return (y, x)  # Retorna las coordenadas (y, x)

        
                
    def distancia_manhattan(self, A, B):
        return abs(A[0] - B[0]) + abs(A[1] - B[1])



    def is_valid(self, x, y, grid):
        """
        Verifica si una posición (x, y) en el grid es válida para moverse.

        Parámetros:
        x (int): Coordenada en el eje x (fila).
        y (int): Coordenada en el eje y (columna).
        grid (list de listas): El grid que representa el entorno.

        Retorna:
        bool: Retorna True si la posición es válida (dentro de los límites del grid y no es una pared), 
              de lo contrario, retorna False.
        """
        return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != 1



    def add_node(self, tree, path, next_cost, node, picked_up_passenger, next_direction_name):
        """
        Añade un nodo al árbol de búsqueda en la posición indicada por el path.

        Parámetros:
        tree (list): El árbol de búsqueda, representado como una lista de nodos.
        path (list): Ruta de índices para acceder al nodo correcto dentro del árbol.
        next_cost (int, float): Costo del nodo que se va a añadir.
        node (tuple): Coordenadas del nodo que se va a añadir (x, y).
        picked_up_passenger (bool): Indica si el pasajero ha sido recogido (True/False).
        next_direction_name (str): Nombre de la dirección hacia la cual se ha movido (arriba, abajo, izquierda, derecha).

        Retorna:
        list: El árbol de búsqueda actualizado con el nuevo nodo agregado.
        """
        # Si el path está vacío, añade el nuevo nodo como un hijo del nodo raíz
        if not path:
            tree[0][2].append((next_cost, node, [], picked_up_passenger, next_direction_name))
            return tree

        # Navega por el árbol usando el path y añade el nodo en la ubicación correcta
        subtree = tree[0][2]
        for i, index in enumerate(path):
            subtree = subtree[index][2]
            # Cuando se llega a la última posición en el path, se agrega el nuevo nodo
            if i + 1 == len(path):
                subtree.append((next_cost, node, [], picked_up_passenger, next_direction_name))
        return tree



    def search_A(self, grid, start, goal):
        """
        Realiza una búsqueda de costo mínimo en el grid desde un nodo inicial hasta el nodo objetivo.

        Parámetros:
        grid (list de listas): El grid que representa el entorno con diferentes tipos de celdas.
        start (tuple): Coordenadas (x, y) del nodo inicial.
        goal (tuple): Coordenadas (x, y) del nodo objetivo.

        Retorna:
        tuple: Una tupla que contiene:
            - tree (list): El árbol de búsqueda con todos los nodos expandidos.
            - path (list): La lista de índices que indica la ruta desde el inicio hasta el objetivo.
            - total_cost (int, float): El costo total del camino más corto encontrado.
        """
        # Inicializa la cola de prioridad, el árbol de búsqueda y la lista de nodos visitados
        priority_queue = []
        tree = [(self.distancia_manhattan(start, self.passenger), start, [], False, "start")]
        heapq.heappush(priority_queue, (self.distancia_manhattan(start, self.passenger), start, [], False, "start"))
        visited = [(start, False)]

        self.explored_nodes += 1
        self.max_depth += 1

        # Bucle principal de búsqueda
        while priority_queue:
            current_cost, current_node, path, picked_up_passenger, direction_name = heapq.heappop(priority_queue)
            x, y = current_node
            next_index = 0
            expanded_node_info = [current_node, [], [], picked_up_passenger, [], current_cost, []]


            for i, (dx, dy) in enumerate(self.MOVEMENTS):
                next_x, next_y = x + dx, y + dy

                if self.is_valid(next_x, next_y, grid):
                    if ((next_x, next_y), picked_up_passenger) not in visited:
                        next_node = (next_x, next_y)
                        next_path = path + [next_index]
                        next_direction_name = self.DIRECTIONS[i]

                        has_passenger = True if next_node == self.passenger and not picked_up_passenger else picked_up_passenger

                        
                        next_cost = current_cost + self.COSTS[grid[next_x][next_y]] + self.distancia_manhattan(next_node, self.goal if has_passenger else self.passenger)


                        heapq.heappush(priority_queue, (next_cost, next_node, next_path, has_passenger, next_direction_name))
                        tree = self.add_node(tree, path, next_cost, next_node, has_passenger, next_direction_name)
                        visited.append((next_node, has_passenger))

                        expanded_node_info[1].append(next_node)
                        expanded_node_info[2].append(next_direction_name)
                        expanded_node_info[4].append(has_passenger)
                        expanded_node_info[6].append(next_cost)


                        self.explored_nodes += 1
                        self.max_depth = max(self.max_depth, (len(next_path) + 1))

                        if next_node == goal and picked_up_passenger:
                            self.final_nodes.append([expanded_node_info])
                            return tree, next_path, next_cost

                        next_index += 1

            self.final_nodes.append([expanded_node_info])

        return tree, [], 0



    def print_classic_tree(self, node, prefix="", is_last=True):
        """
        Genera una representación en texto del árbol de búsqueda.

        Parámetros:
        node (list): El nodo raíz del árbol de búsqueda.
        prefix (str): Prefijo utilizado para construir el árbol visualmente.
        is_last (bool): Indica si el nodo actual es el último en su nivel.

        Retorna:
        str: El árbol de búsqueda en formato de texto.
        """
        result = []
        try:
            cost, coord, children, has_passenger, direction_name = node
        except:
            cost, coord, children, has_passenger, direction_name = node[0]

        connector = "--> " if is_last else "|-- "
        result.append(f"{prefix}{connector}{coord} [cost: {cost}] [Passenger? {has_passenger}] [Direction: {direction_name}]")

        if children:
            new_prefix = prefix + ("    " if is_last else "|   ")
            for i, child in enumerate(children):
                result.append(self.print_classic_tree(child, new_prefix, i == len(children) - 1))

        return "\n".join(result)



    def generate_path_output(self, final_tree, path):
        """
        Genera la salida que representa el camino desde el nodo inicial hasta el objetivo.

        Parámetros:
        final_tree (list): El árbol de búsqueda completo.
        path (list): El camino de índices que indica la ruta óptima en el árbol.

        Retorna:
        list: Una lista de tuplas que contiene las coordenadas del nodo, la dirección y el costo en cada paso.
        """
        node = final_tree[0]
        cost, coord, children, has_passenger, direction_name = node
        output = [(self.start, "", 0)]

        children = node[2]
        for i, step in enumerate(path):
            node = children[step]
            cost, coord, children, has_passenger, direction_name = node
            output.append((coord, direction_name, cost))

        return output



    def solve(self):
        """
        Resuelve el problema de búsqueda del camino óptimo desde el inicio hasta el objetivo, recogiendo al pasajero.

        Retorna:
        dict: Un diccionario con la siguiente información:
            - "tree": El árbol de búsqueda en formato de texto.
            - "path": La lista de pasos que conforman el camino encontrado.
            - "total_cost": El costo total del camino encontrado.
            - "explored_nodes": El número de nodos explorados durante la búsqueda.
            - "max_depth": La profundidad máxima alcanzada en la búsqueda.
            - "computation_time": El tiempo de cómputo total para realizar la búsqueda.
            - "expanded_nodes": Información sobre los nodos expandidos en la búsqueda.
        """
        start_time = time.time()
        final_tree, path, total_cost = self.search_A(self.grid, self.start, self.goal)
        end_time = time.time()
        computation_time = end_time - start_time

        return {
            "tree": self.print_classic_tree(final_tree),
            "path": self.generate_path_output(final_tree, path),
            "total_cost": total_cost,
            "explored_nodes": self.explored_nodes,
            "max_depth": self.max_depth,
            "computation_time": f"{computation_time:.5f} seconds",
            "expanded_nodes": self.final_nodes
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
