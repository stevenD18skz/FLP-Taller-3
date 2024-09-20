import pprint
import pygame 
from settings import *
from tile import Tile
from debug import debug
from support import *
from random import choice
from player import Player
from code.Logic.viejo.CostoSearch import COSTOSEARCH
from code.Logic.viejo.AmplitudSearch import BusquedaAmplitud


#COSTOSEARCH

class Level:
    def __init__(self):
        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()


        self.entrada1 =  [
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

        self.entrada2 = [
            [0, 1, 1, 1, 0, 0, 4, 0, 0, 6],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [2, 0, 1, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 3, 0, 0],
            [0, 1, 1, 0, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 5],
            [0, 0, 0, 0, 1, 0, 4, 1, 1, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 1, 1, 1]
        ]

        self.entrada3 = [
            [0, 1, 1, 1, 0, 0, 1, 4, 0, 1, 0, 6],
            [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5],
            [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0]
        ]

        self.entrada4 = [
            [0, 1, 1, 0, 0, 1, 4, 0, 0, 0, 0, 0, 1, 1, 6],
            [1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
            [2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
            [0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1],
            [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
            [5, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
        ]

        self.entrada5 = [
            [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 6],
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0],
            [0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0],
            [2, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            [0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1],
            [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
            [0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1],
            [5, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0]
        ]

        self.entrada6 = [
            [0, 1, 0, 0, 0, 1, 4, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 6],
            [1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1],
            [0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 5],
            [0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        ]


        self.motor = None

        # sprite setup
        self.create_map()
        self.z_pressed = False  # Variable para controlar si ya se presionó la tecla
        




    def input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_z] and not self.z_pressed:
            # Ejecutar la lógica solo una vez cuando se presiona la tecla Z
            solucion = self.motor.solucionar()
            print(f"solucion {solucion}")
            self.player.movimientos = solucion
            self.z_pressed = True  # Marcar que la tecla Z ha sido presionada

        if not key[pygame.K_z]:
            # Resetear la variable cuando se suelta la tecla Z
            self.z_pressed = False



    def create_map(self):
        layout = self.entrada1 # cargar txt
        graphics = import_folder(path_main + 'graphics/objects')
        self.motor = BusquedaAmplitud(layout)



        llave_nombre = {
            1: "pasto",
            2: "lapras",
            3: "snorlax_dormido",
            4: "snorlax_despierto",
            5: "net",
            6: "meta",
        }

        """     
        • 0 si es una casilla libre (tráfico liviano) 
        • 1 si es un muro 
        • 2 si es el punto de partida del vehículo 
        • 3 si es una casilla con tráfico medio 
        • 4 si es una casilla con tráfico pesado 
        • 5 si es el pasajero 
        • 6 si es el destino del pasajero
        """


        for row_index,row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE

                    if int(col) == 0:
                        pass

                    elif int(col) == 2:
                        self.player = Player(
                            (self.motor.encontrar_objeto(2)[0] * TILESIZE, self.motor.encontrar_objeto(2)[1] * TILESIZE),
                            [self.visible_sprites],self.obstacle_sprites, 
                            (TILESIZE, TILESIZE))
                    
                    else:
                        surf = pygame.transform.scale(graphics[llave_nombre[int(col)]], (TILESIZE, TILESIZE))
                        Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)




    def run(self):
        self.input()
        self.visible_sprites.custom_draw()
        self.visible_sprites.update()
        debug(f"{self.player.status} === {self.player.rect} === {self.player.movimiento_actual}")






class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup 
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # creating the floor
        self.floor_surf = pygame.image.load(path_main + "graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))



    def custom_draw(self):
        # dibuja el suelo (escenario fijo)
        self.display_surface.blit(self.floor_surf, self.floor_rect.topleft)

        # Crea una lista de sprites ordenada por la coordenada Y
        sprites_ordenados = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)

        # Dibuja todos los sprites en el orden de la lista
        for sprite in sprites_ordenados:
            #dibujar las areas para debug
            try:
                pass
                #pygame.draw.rect(self.display_surface, (0, 100, 0), sprite.activacion)
                #pygame.draw.rect(self.display_surface, (40, 48, 48), sprite.rect)
                #pygame.draw.rect(self.display_surface, (255, 0, 0), sprite.hitbox)
            except:
                pass
                #pygame.draw.rect(self.display_surface, (40, 48, 48), sprite.rect)
                #pygame.draw.rect(self.display_surface, (255, 0, 0), sprite.hitbox)

            if isinstance(sprite, Player):
                pygame.draw.rect(self.display_surface, (255, 0, 0), sprite.hitbox)
                pygame.draw.rect(self.display_surface, (40, 48, 48), sprite.rect)

            # Dibuja la imagen del sprite
            self.display_surface.blit(sprite.image, sprite.rect.topleft)
