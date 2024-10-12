import heapq
import time


class CostSearch():
    def __init__(self, grid):
        # Constants
        self.START_REPRESENTATION = 2
        self.PASSENGER_REPRESENTATION = 5
        self.GOAL_REPRESENTATION = 6

        # Define movements (up, down, left, right)
        self.MOVEMENTS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.DIRECTIONS = ["up", "down", "left", "right"]

        # Initialize the grid
        self.grid = grid
        self.start = self.find_object(self.START_REPRESENTATION)
        self.passenger = self.find_object(self.PASSENGER_REPRESENTATION)
        self.goal = self.find_object(self.GOAL_REPRESENTATION)

        # Tree search data
        self.explored_nodes = 0
        self.max_depth = 0

        # Cost mapping
        self.COSTS = {
            0: 1,   # Free space
            1: float('inf'),  # Wall (inaccessible)
            2: 1,   # Start point
            3: 8,   # Medium traffic
            4: 15,  # Heavy traffic
            5: 1,   # Passenger
            6: 1    # Goal
        }

        # Tree visualization data
        self.carry_depth = 0
        self.current_nodes = []
        self.final_nodes = []



    def find_object(self, object_value):
        for y, row in enumerate(self.grid):
            for x, value in enumerate(row):
                if value == object_value:
                    return (y, x)



    def is_valid(self, x, y, grid):
        return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != 1



    def add_node(self, tree, path, next_cost, node, picked_up_passenger, next_direction_name):
        # Add node at root if path is empty
        if not path:
            tree[0][2].append((next_cost, node, [], picked_up_passenger, next_direction_name))
            return tree

        # Navigate the tree to the correct depth
        subtree = tree[0][2]
        for i, index in enumerate(path):
            subtree = subtree[index][2]
            if i + 1 == len(path):
                subtree.append((next_cost, node, [], picked_up_passenger, next_direction_name))
        return tree



    def search_cost(self, grid, start, goal):
        priority_queue = []
        tree = [(0, start, [], False, "start")]
        heapq.heappush(priority_queue, (0, start, [], False, "start"))
        visited = [(start, False)]

        self.explored_nodes += 1
        self.max_depth += 1

        while priority_queue:
            current_cost, current_node, path, picked_up_passenger, direction_name = heapq.heappop(priority_queue)
            x, y = current_node
            next_index = 0

            expanded_node_info = [current_node, [], [], picked_up_passenger, current_cost, []]
            for i, (dx, dy) in enumerate(self.MOVEMENTS):
                next_x, next_y = x + dx, y + dy

                if self.is_valid(next_x, next_y, grid):
                    if ((next_x, next_y), picked_up_passenger) not in visited:
                        next_node = (next_x, next_y)
                        next_path = path + [next_index]
                        next_direction_name = self.DIRECTIONS[i]
                        next_cost = current_cost + self.COSTS[grid[next_x][next_y]]

                        has_passenger = True if next_node == self.passenger and not picked_up_passenger else picked_up_passenger

                        # Add node to queue, tree, and visited list
                        heapq.heappush(priority_queue, (next_cost, next_node, next_path, has_passenger, next_direction_name))
                        tree = self.add_node(tree, path, next_cost, next_node, has_passenger, next_direction_name)
                        visited.append((next_node, has_passenger))

                        expanded_node_info[1].append(next_node)
                        expanded_node_info[2].append(next_direction_name)
                        expanded_node_info[5].append(next_cost)

                        # Update tree and search stats
                        self.explored_nodes += 1
                        self.max_depth = max(self.max_depth, (len(next_path) + 1))

                        if next_node == goal and picked_up_passenger:
                            return tree, next_path, next_cost

                        next_index += 1

            self.final_nodes.append([expanded_node_info])

        return tree, [], 0



    def print_classic_tree(self, node, prefix="", is_last=True):
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
        node = final_tree[0]
        cost, coord, children, has_passenger, direction_name = node
        output = []

        children = node[2]
        for i, step in enumerate(path):
            node = children[step]
            cost, coord, children, has_passenger, direction_name = node
            output.append((coord, direction_name))

        return output



    def solve(self):
        # Search for path to the goal
        start_time = time.time()
        final_tree, path, total_cost = self.search_cost(self.grid, self.start, self.goal)
        end_time = time.time()
        computation_time = end_time - start_time

        # Return the solution data
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
