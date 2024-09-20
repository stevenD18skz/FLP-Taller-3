import pygame
from os import walk
from os.path import splitext
from csv import reader
import pygame

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

