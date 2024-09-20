def imprimir_arbol_grafico(arbol, prefijo="", es_ultimo=True):
    # Desempaqueta los elementos del nodo
    nodo, hijos, *extra = arbol
    
    # Imprime el nodo actual con el prefijo correcto para mostrar las conexiones
    print("\n0",end="")
    print(prefijo + ("└── " if es_ultimo else "├── ") + f"{nodo}", end="")

    # Actualiza el prefijo para los hijos
    prefijo += "    " if es_ultimo else "│   "
    
    # Recorre los hijos y los imprime recursivamente


    print("\n1",end="")
    siguiente_fila = []
    for i, hijo in enumerate(hijos):
        print(prefijo + ("└── " if es_ultimo else "├── ") + f"{hijo[0]}", end="")
        siguiente_fila.append(hijo)


    print("\n2",end="")
    main = siguiente_fila
    siguiente_fila = []
    for i, hijo in enumerate(main): # [(A [B, C]), (G [R, T])]
        if i != 0:
            print(f"{" "*(40 - (len(hijo[1]) * 4))}", end="")
            
        for x, impri in enumerate(hijo[1]):
            print("  ", end="")
            print(prefijo + ("└── " if es_ultimo else "├── ") + f"{impri[0]}", end="")
            siguiente_fila.append(impri)
        


    print("\n3",end="")
    main = siguiente_fila
    siguiente_fila = []
    for i, hijo in enumerate(main):
        if i != 0:
            print(f"{" "*(40 - (len(hijo[1]) * 4))}", end="")
            
        for x, impri in enumerate(hijo[1]):
            print("  ", end="")
            print(prefijo + ("└── " if es_ultimo else "├── ") + f"{impri[0]}", end="")
            siguiente_fila.append(impri)


    print("\n4",end="")
    main = siguiente_fila
    siguiente_fila = []
    for i, hijo in enumerate(main):
        if i != 0:
            print(f"{" "*(40 - (len(hijo[1]) * 4))}", end="")
            
        for x, impri in enumerate(hijo[1]):
            print("  ", end="")
            print(prefijo + ("└── " if es_ultimo else "├── ") + f"{impri[0]}", end="")
            siguiente_fila.append(impri)



       # imprimir_arbol_grafico(hijo, prefijo, es_ultimo_hijo)




# Estructura del árbol de ejemplo
arbol_binario = ((2, 0), [
    ((1, 0), [
        ((0, 0), [], False, 'arriba')
    ], False, 'arriba'),
    ((3, 0), [
        ((4, 0), [
            ((5, 0), [
                ((6, 0), [
                    ((5, 0), [
                        ((4, 0), [], True, 'arriba'),
                        ((6, 0), [], True, 'abajo')
                    ], True, 'arriba'),
                    ((7, 0), [], True, 'abajo')
                ], False, 'abajo'),
                ((5, 1), [
                    ((5, 2), [], False, 'derecha')
                ], False, 'derecha')
            ], False, 'abajo')
        ], False, 'abajo'),
        ((3, 1), [
            ((3, 2), [
                ((3, 3), [
                    ((2, 3), [], False, 'arriba'),
                    ((4, 3), [], False, 'abajo'),
                    ((3, 4), [], False, 'derecha')
                ], False, 'derecha')
            ], False, 'derecha')
        ], False, 'derecha')
    ], False, 'abajo')
], False, 'start')

# Llamada a la función
#imprimir_arbol_grafico(arbol_binario)


cadena = "A"




# Convertirla en una lista
cadena = cadena.split(" ")

i = 3

cadena = [f"{"="*int((24*4/2))}A",
          f"{"="*int((24*2/2))}B{"="*int((24*2/2))}{"+"*int((24*2/2))}C{"="*int((24*2/2))}",
          f"{"="*int((24*1/2))}D{"="*int((24*1/2))}{"+"*int((24*1/2))}G{"="*int((24*1/2))}{"+"*int((24*1/2))}{"="*int((24*1/2))}I{"="*int((24*2/2))}",
          f"{"="*int((24*1/1))}{"+"*int((24*0/2))}C{"="*int((24*2/2))}",
        ]



#for i, x in enumerate(cadena):
#    cadena[i] = x.rjust(30, " ")

#print("\n".join(cadena))


cadena = [f"{" "*int((24*2/2))}A",
          f"{" "*int((24*1/2))}B{" "*int((24*1/2))}{" "*int((24*1/2))}C{" "*int((24*1/2))}",
          f"{" "*int((24*1/3))}D{" "*int((24*1/3))}G{" "*int((24*1/3))}{" "*int((24*0/2))}{" "*int((24*1/2))}I{" "*int((24*1/2))}"]



#print("\n".join(cadena))

i = 2
cadena = [f"{"="*int((24*i/2))}A",
          f"{"="*int((24*i/3))}B{"="*int((24*i/3))}C{"="*int((24*i/3))}"]



#print("\n".join(cadena))

nodos = ("A", [("B", [("D", []), ("G", [])]), ("C", [("I", [])])])

siguiente_fila = [('B', [('D', []), ('E', [])]), ('C', [('F', [])])]

siguiente_fila = [('B', [('D', []), ('E', [])])]


from collections import defaultdict

def calculate_positions(tree, level=0, pos=0, result=None, width=100):
    if result is None:
        result = defaultdict(list)

    node, children = tree

    # Guardamos el nodo en su nivel y posición
    result[level].append((pos, node))

    if children:
        num_children = len(children)
        # Distribuimos el espaciado según el número de hijos
        spacing = width // max(1, num_children + 1)
        for i, child in enumerate(children):
            # Calculamos la posición del hijo
            child_pos = pos + (i - num_children // 2) * spacing
            calculate_positions(child, level + 1, child_pos, result, width // 2)

    return result

def display_tree(tree):
    levels = calculate_positions(tree)
    max_level = max(levels.keys())

    for level in range(max_level + 1):
        current_level = sorted(levels[level], key=lambda x: x[0])  # Ordenamos por posición
        level_str = ""
        last_pos = 0
        for pos, node in current_level:
            # Agregamos espacios en función de la posición del nodo
            level_str += " " * (pos - last_pos) + node
            last_pos = pos + 1
        print(level_str)

nodos = ("A", [
    ("B", [("D", [("F", [])]), ("G", []), ("R", [])]), 
    ("C", [("I", [("T", []), ("P", [])])]), 
    ("Z", [("M", [])])
])

display_tree(nodos)



"""
                             A
       B                     C                   Z
D            G               I                   M
F                            T

[((1, 0), [((0, 0), [], False, 'arriba')], False, 'arriba'), ((3, 0), [((4, 0), [((5, 0), [((6, 0), [((5, 0), [((4, 0), [], True, 'arriba'), ((6, 0), [], True, 'abajo')], True, 'arriba'), ((7, 0), [], True, 'abajo')], False, 'abajo'), ((5, 1), [((5, 2), [], False, 'derecha')], False, 'derecha')], False, 'abajo')], False, 'abajo'), ((3, 1), [((3, 2), [((3, 3), [((2, 3), [], False, 'arriba'), ((4, 3), [], False, 'abajo'), ((3, 4), [], False, 'derecha')], False, 'derecha')], False, 'derecha')], False, 'derecha')], False, 'abajo')]


└── (2, 0) [P? False] [direccion start]
    ├── (1, 0) [P? False] [direccion arriba]
    │   └── (0, 0) [P? False] [direccion arriba]
    └── (3, 0) [P? False] [direccion abajo]
        ├── (4, 0) [P? False] [direccion abajo]
        │   └── (5, 0) [P? False] [direccion abajo]
        │       ├── (6, 0) [P? False] [direccion abajo]
        │       │   ├── (5, 0) [P? True] [direccion arriba]
        │       │   │   ├── (4, 0) [P? True] [direccion arriba]
        │       │   │   └── (6, 0) [P? True] [direccion abajo]
        │       │   └── (7, 0) [P? True] [direccion abajo]
        │       └── (5, 1) [P? False] [direccion derecha]
        │           └── (5, 2) [P? False] [direccion derecha]
        └── (3, 1) [P? False] [direccion derecha]
            └── (3, 2) [P? False] [direccion derecha]
                └── (3, 3) [P? False] [direccion derecha]
                    ├── (2, 3) [P? False] [direccion arriba]
                    ├── (4, 3) [P? False] [direccion abajo]
                    └── (3, 4) [P? False] [direccion derecha]

                    

                                                        ├── (2, 0) [P? False] [direccion start]

                        ├── (1, 0) [P? False] [direccion arriba]                   ├── (3, 0) [P? False] [direccion abajo]
                        │                                                          │
                        └── (0, 0) [P? False] [direccion arriba]                   ├── (4, 0) [P? False] [direccion abajo]

                                                                        └── (5, 0) [P? False] [direccion abajo]             └── (5, 1) [P? False] [direccion derecha]

"""