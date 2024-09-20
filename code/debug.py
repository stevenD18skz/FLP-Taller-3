import pygame
from settings import *
pygame.init()

font_path = path_main + "graphics/font/PKMN RBYGSC.ttf"  # Actualiza esto con la ruta correcta
font = pygame.font.Font(font_path, 30)



font = pygame.font.Font(None,30)


"""
    Muestra información de un dato especifico
	en tipo depuración en la pantalla.
"""
def debug(info,y = 10, x = 10):
	display_surface = pygame.display.get_surface()
	debug_surf = font.render(str(info),True,'White')
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	pygame.draw.rect(display_surface,'Black',debug_rect)
	display_surface.blit(debug_surf,debug_rect)
