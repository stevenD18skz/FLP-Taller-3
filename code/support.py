import pygame
import os
from os import walk
from os.path import splitext
from csv import reader
import pygame



CASILLA_SIZE = 64
CUADRADO_SIZE = 32
CUADRADO_SIZE = 32
FLECHA_ANCHO = 16
FLECHA_ALTO_VERTICAL = 32
TEXT_COLOR = (255, 255, 255)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)



"""
Importa un archivo CSV que contiene un diseño de terreno y lo convierte en una lista bidimensional.

Parámetros:
    path (str): La ruta del archivo CSV que se va a importar.

Retorna:
    list: Una lista bidimensional que representa el diseño del terreno.
"""
def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


"""
Importa imágenes de una carpeta y las convierte en superficies de Pygame
para guardarlas en una lista.

Parámetros:
    path (str): La ruta de la carpeta que contiene las imágenes a importar.

Retorna:
    list: Una lista de superficies de Pygame.
"""

def import_folder_un(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def import_folder(path):
    surface_dict = {}
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_name = splitext(image)[0]  # Obtener el nombre sin la extensión
            surface_dict[image_name] = image_surf
    return surface_dict

def ALFile(ruta_archivo=""):
    if ruta_archivo == "":
        return ""

    with open(ruta_archivo, 'r') as archivo:
        # Leer cada línea del archivo, dividirla por espacios y convertir los valores a enteros
        mapa = [list(map(int, linea.split())) for linea in archivo]
    
    return mapa



# Función para calcular la posición central de una casilla
def centrar_en_casilla(coordenadas):
    y, x = coordenadas
    transformacion = (x * CASILLA_SIZE, y * CASILLA_SIZE)
    centro = (transformacion[0] + CASILLA_SIZE // 2 - CUADRADO_SIZE // 2,
            transformacion[1] + CASILLA_SIZE // 2 - CUADRADO_SIZE // 2)
    return centro


# Función para calcular la posición de la flecha
def calcular_posicion_flecha(centro, direccion, tamano_flecha):
    if direccion == "arriba":
        return (centro[0] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2, centro[1] - tamano_flecha)
    elif direccion == "abajo":
        return (centro[0] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2, centro[1] + CUADRADO_SIZE)
    elif direccion == "izquierda":
        return (centro[0] - tamano_flecha, centro[1] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2)
    elif direccion == "derecha":
        return (centro[0] + CUADRADO_SIZE, centro[1] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2)


# Función para obtener el tamaño de la flecha según la dirección
def obtener_tamano_flecha(direccion, alpha):
    if direccion == "arriba" or direccion == "abajo":
        return (FLECHA_ANCHO, int(FLECHA_ALTO_VERTICAL*alpha))     #(ancho, alto)
    elif direccion == "izquierda" or direccion == "derecha":
        return (int(FLECHA_ALTO_VERTICAL*alpha), FLECHA_ANCHO)


def calcular_posicion_flecha_final(centro, direccion, tamano_flecha):
    if direccion == "abajo":
        return (centro[0] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2, centro[1] - tamano_flecha)
    elif direccion == "arriba":
        return (centro[0] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2, centro[1] + CUADRADO_SIZE)
    elif direccion == "derecha":
        return (centro[0] - tamano_flecha, centro[1] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2)
    elif direccion == "izquierda":
        return (centro[0] + CUADRADO_SIZE, centro[1] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2)