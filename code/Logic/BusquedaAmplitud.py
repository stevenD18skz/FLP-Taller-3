import time



class BusquedaAmplitud():
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
        self.acarreo_profundidad = 0



    def encontrar_objeto(self, valor_objeto): #hay que acomodarla (y, x) => (x, y)
        for y, array in enumerate(self.mapa):
            for x, valor in enumerate(array):
                if valor == valor_objeto:
                    return (y, x)



    def is_valid(self, x, y, grid):
        return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != 1


              
    def agregar_nodo(self, ARBOL, path, nodo, picked_up_passenger, next_dir_name):
            # Si no hay coordenadas, estamos en la raíz, y agregamos directamente
            if not path:
                ARBOL[0][1].append((nodo, [], picked_up_passenger, next_dir_name))
                #imprimir_arbol_clasico(tree)
                return ARBOL
            

            # Empezamos desde el primer nivel de profundidad (sin contar la raíz)
            sub_tree = ARBOL[0][1]
            for i, c in enumerate(path):
                # Encontramos el nodo que corresponde a 'c' 
                #       [A, [K, L, J]] => c es por asi decir el hijo de A que esa en la c-nesima posicion
                #       en este caso si c fuera 2, el hijo seleccionado seria J
                sub_tree = sub_tree[c][1]

                # Si estamos en el último índice de 'cor', agregamos el nuevo nodo, 
                # esto es que ya llegamos a donde queriamos llegar
                if i + 1 == len(path):
                    sub_tree.append((nodo, [], picked_up_passenger, next_dir_name))
            
            return ARBOL



    def search_cost(self, grid, start, goal):
        CP = []#la cola de nodos a evular

        #UN NODO ES IGUAL A = COORDENADA HIJOS up_passager DIRECCION
        ARBOL = [(start, [], False, "start")]   #El arbol de busqueda
        CP.append((start, [], False,  "start")) #Cola de nodos por expandir
        visited = [(start, False)]              #nodos visitados (nodo, si es un camino con el pasajero recogido)

        self.nodos_expandidos += 1
        self.profunidad_maxima = 1
        
        while CP:
            if self.acarreo_profundidad == len(CP[0][1]):
                #print(f"Cola: {CP} Profundida {self.acarreo_profundidad}")
                self.acarreo_profundidad += 1
                #print(self.imprimir_arbol_clasico(ARBOL))
                #input()

            current_node, path, picked_up_passenger, dir_name = CP.pop(0) #crear nodo actual
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

                        if next_node == self.passager and not picked_up_passenger:
                            CP.append((next_node, next_path, True, next_dir_name))
                            ARBOL = self.agregar_nodo(ARBOL, path, next_node, True, next_dir_name)
                            visited.append(((next_node), True))
                        
                        else:
                            CP.append((next_node, next_path, picked_up_passenger, next_dir_name))
                            ARBOL = self.agregar_nodo(ARBOL, path, next_node, picked_up_passenger, next_dir_name)
                            visited.append(((next_node), picked_up_passenger))
                        
                        #se ajustan valores de salida de informacion
                        self.nodos_expandidos += 1
                        self.profunidad_maxima = max(self.profunidad_maxima, (len(next_path) + 1))

                        if next_node == goal and picked_up_passenger:
                            return ARBOL, next_path
                        
                        indice += 1

        return ARBOL, []



    def imprimir_arbol_clasico(self, lista, prefijo="", es_ultimo=True):
        resultado = []  # Lista para acumular las cadenas generadas
        try:
            nodo, hijos, up, dir_name = lista
        except:
            nodo, hijos, up, dir_name = lista[0]

        marcador = "--> " if es_ultimo else "|-- "
        resultado.append(prefijo + marcador + f"{nodo}")#[P? {up}] [direccion {dir_name}]")

        if hijos:
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "|   ")
            for i, hijo in enumerate(hijos):
                resultado.append(self.imprimir_arbol_clasico(hijo, nuevo_prefijo, i == len(hijos) - 1))

        return "\n".join(resultado)  # Unir todas las cadenas y devolver



    def crear_salida_gui(self, arbol_final, camino_arbol):
        #costo nodo hijos
        nodo = arbol_final[0]
        cord, hijos, up, dir_name = nodo
        res = []

        hijos = nodo[1]
        for i, c in enumerate(camino_arbol):
            nodo = hijos[c]
            cord, hijos, up, dir_name  = nodo
            res.append((cord, dir_name))

        return res



    def solucionar(self):
        #encontrar camino hasta el pasajero
        tiempo_inicio = time.time()
        arbol_final, camino_arbol = self.search_cost(self.mapa, self.start, self.goal)
        tiempo_final = time.time()
        tiempo_computo = tiempo_final - tiempo_inicio  

        #devolver el camino completo
        return {
            "arbol":  self.imprimir_arbol_clasico(arbol_final),
            "paths": self.crear_salida_gui(arbol_final, camino_arbol),
            "nodos_explorados": self.nodos_expandidos,
            "profundidad_maxima": self.profunidad_maxima,
            "tiempo_computo": f"{tiempo_computo:6.5f}"
        }





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

# Imprimimos los caminos encontrados
print("Caminos encontrados a los objetivos:")
print(f"Pasos Necesarios: {len(solucion["paths"])}")
print(f"Nodos explorados: {solucion['nodos_explorados']}")
print(f"Profundidad máxima del árbol: {solucion['profundidad_maxima']}")
print(f"Tiempo de cómputo: {solucion['tiempo_computo']} (S)")
print(f"\nCAMINO:\n{solucion["paths"]}")
print(f"\n\nARBOL:\n{solucion["arbol"]}")
