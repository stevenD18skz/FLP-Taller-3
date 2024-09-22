import pygame 
from settings import *
from tile import Tile
from debug import debug
from support import *
from random import choice
from player import Player

from Logic.Prueba import BusquedaAmplitud
from Logic.Costo_1 import Costo
from Logic.Profundidad_WN import BusquedaProfundidad


#COSTOSEARCH

class Level:
    def __init__(self):
        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.mapa = None
        self.motor = None

        # Variables para la animación de texto
        self.text_alpha = 255  # Opacidad inicial
        self.fade_speed = 5    # Velocidad de desvanecimiento
        self.fading_out = True  # Control de la animación de desvanecimiento

        self.z_pressed = False  # Variable para controlar si ya se presionó la tecla


    """
    def input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_z] and not self.z_pressed:
            # Ejecutar la lógica solo una vez cuando se presiona la tecla Z
            solucion = self.motor.solucionar()
            self.player.movimientos = solucion
            self.z_pressed = True  # Marcar que la tecla Z ha sido presionada

        if not key[pygame.K_z]:
            # Resetear la variable cuando se suelta la tecla Z
            self.z_pressed = False
    """
    
    def ejecutarAlgoritmo(self, eleccion):
        algoritmos = {
            "Amplitud": BusquedaAmplitud,
            "Costo uniforme": Costo,
            "Profundidad evitando ciclos": BusquedaProfundidad,
            "Avara": None,
            "A*": None,
        }

        motor = algoritmos[eleccion](self.mapa)
        solucion = motor.solucionar()

        self.player.movimientos = solucion["paths"]

        return solucion



    def create_map(self):
        layout = self.mapa
        graphics = import_folder(path_main + 'graphics/objects')
        self.motor = BusquedaAmplitud(layout)



        llave_nombre = {
            1: ["pasto", "object"],
            2: ["lapras", "object"],
            3: ["snorlax_dormido", "object"],
            4: ["snorlax_despierto", "object"],
            5: ["net", "passager"],
            6: ["meta", "goal"],
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
                            (self.motor.encontrar_objeto(2)[1] * TILESIZE, self.motor.encontrar_objeto(2)[0] * TILESIZE),
                            [self.visible_sprites],
                            self.obstacle_sprites, 
                            (TILESIZE, TILESIZE))
                    
                    else:
                        surf = pygame.transform.scale(graphics[llave_nombre[int(col)][0]], (TILESIZE, TILESIZE))
                        Tile((x,y),
                             [self.visible_sprites,self.obstacle_sprites],
                             llave_nombre[int(col)][1],
                             surf)



    def loading_screen(self):
        screen_width = 640
        screen_height = 640

        # Colores
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GREY = (100, 0, 0)
        
        # Fuente
        font = pygame.font.Font(None, 50)

        # Fondo de la pantalla
        #self.display_surface.fill(GREY)

        # Dibujar el recuadro negro con bordes redondeados
        rect_width = 640
        rect_height = 640
        rect_x = (screen_width - rect_width) // 2
        rect_y = (screen_height - rect_height) // 2
        pygame.draw.rect(self.display_surface, BLACK, (rect_x, rect_y, rect_width, rect_height), border_radius=25)

        # Crear el texto "esperando entrada"
        text_surface = font.render("esperando entrada", True, WHITE)
        text_surface.set_alpha(self.text_alpha)  # Ajustar la transparencia
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))

        # Dibujar el texto
        self.display_surface.blit(text_surface, text_rect)

        # Control de la animación (aparecer/desaparecer)
        if self.fading_out:
            self.text_alpha -= self.fade_speed
            if self.text_alpha <= 0:
                self.text_alpha = 0
                self.fading_out = False
        else:
            self.text_alpha += self.fade_speed
            if self.text_alpha >= 255:
                self.text_alpha = 255
                self.fading_out = True


    def run(self):
        if self.mapa == None:
            self.loading_screen()
            return

        #print("1111111111111111")
        self.visible_sprites.custom_draw()#4
        #print("2222222222222222")
        self.visible_sprites.update()
        #print("55555555555555555")
        debug(f"{self.player.status} === {self.player.rect} === {self.player.movimiento_actual}")
    

    def setMap(self, map):
        self.mapa = map
        self.create_map()






class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup 
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # creating the floor
        self.floor_surf = pygame.transform.scale(pygame.image.load(path_main + "graphics/tilemap/ground.png").convert(), (640, 640))
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))



    def custom_draw(self):
        #print("444444444444444444444s")
        # dibuja el suelo (escenario fijo)
        self.display_surface.blit(self.floor_surf, self.floor_rect.topleft)

        # Crea una lista de sprites ordenada por la coordenada Y
        sprites_ordenados = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)

        # Dibuja todos los sprites en el orden de la lista
        for sprite in sprites_ordenados:
            #dibujar las areas para debug

            if isinstance(sprite, Player):
                pygame.draw.rect(self.display_surface, (255, 0, 0), sprite.hitbox)
                pygame.draw.rect(self.display_surface, (40, 48, 48), sprite.rect)
            
            elif not isinstance(sprite, Player) and sprite.sprite_type == "passager":
                #pygame.draw.rect(self.display_surface, (255, 0, 0), sprite.hitbox)
                pygame.draw.rect(self.display_surface, (40, 48, 48), sprite.rect)
                pygame.draw.rect(self.display_surface, (100, 255, 100), sprite.activacion)
            
            else:
                pygame.draw.rect(self.display_surface, (40, 48, 48), sprite.rect)
                pygame.draw.rect(self.display_surface, (100, 255, 100), sprite.activacion)
            

            # Dibuja la imagen del sprite
            self.display_surface.blit(sprite.image, sprite.rect.topleft)
            
