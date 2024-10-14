import time
from tkinter import font
import pygame 
from settings import *
from tile import Tile
from debug import debug
from support import *
from player import Player

from Logic.BusquedaAmplitud import BusquedaAmplitud
from Logic.BusquedaCosto import CostSearch
from Logic.BusquedaProfundidad import BusquedaProfundidad
from Logic.BusquedaAvara import BusquedaAvara
from Logic.BusquedaAE import BusquedaAE




class Level:
    def __init__(self):
        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.caminos = pygame.sprite.Group()

        #CONTROLADORES DE LOS ALGORITMOS
        self.mapa = None
        self.motor = None

        # Variables para la animación de texto
        self.text_alpha = 255  # Opacidad inicial
        self.fade_speed = 5    # Velocidad de desvanecimiento
        self.fading_out = True  # Control de la animación de desvanecimiento

        #variables control de timepo
        self.arrow_alpha = 0

        self.all_ya = []
        self.all_expandir = []
        self.solucion = None

        self.init_wait = -1 #Manejador de tiempo para la animacino dibujar arbol
        self.init_final = -1 #Manejador de tiempo para la animacino mostrar camino
        self.chat = 0 #Manejador de tiempo para  "arrow_alpha"
        self.time_wait = 0.3
    


    def crear_texto(self, text, tam, tupla):
        self.font = pygame.font.SysFont(None, tam)

        text_surface = self.font.render(text, True, TEXT_COLOR)
        text_surface.set_alpha(self.text_alpha)  # Ajustar la transparencia

        text_rect = text_surface.get_rect(center=(tupla[0] + CUADRADO_SIZE // 2, tupla[1] + CUADRADO_SIZE // 2))

        self.display_surface.blit(text_surface, text_rect)



    def loading_screen(self):
        pygame.draw.rect(self.display_surface, BLACK, (0, 0, 640, 640), border_radius=25)
        self.crear_texto("esperando entrada", 50, (320 - CUADRADO_SIZE, 320 - CUADRADO_SIZE))

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



    def ejecutarAlgoritmo(self, eleccion):
        algoritmos = {
            "Amplitud": BusquedaAmplitud,
            "Costo uniforme": CostSearch,
            "Profundidad evitando ciclos": BusquedaProfundidad,
            "Avara": BusquedaAvara,
            "A*": BusquedaAE,
        }
        
        self.motor = algoritmos[eleccion](self.mapa)
        self.solucion = self.motor.solve()

        self.init_wait = time.time()
        self.chat = time.time()
        self.all_expandir = self.solucion["expanded_nodes"]





    def crear_caminos_arbol(self): 
        def dibujar_cuadro(color, tupla, grosor, costo):
            pygame.draw.rect(self.display_surface, color, pygame.Rect(tupla[0], tupla[1], CUADRADO_SIZE, CUADRADO_SIZE))
            pygame.draw.rect(self.display_surface, VERDE, pygame.Rect(tupla[0], tupla[1], CUADRADO_SIZE, CUADRADO_SIZE), grosor)
            self.crear_texto(str(costo), 24, tupla)


        def dibujar_nodos(ln, ulitma_profundidad):
            for i, n in enumerate(ln):
                #si ultima_profundidad es false entonces son los ya expandidos(rojos), si es true (blue)
                SQUARE_COLOR = ROJO if not ulitma_profundidad else AZUL
                ARROW_COLOR = ROJO if not ulitma_profundidad else AZUL
                SQUARE_COLOR_HIJO = ROJO if not ulitma_profundidad else AZUL
                ESCALAR = 1 if not ulitma_profundidad else self.arrow_alpha

                inicio, hijos, direcciones, up_pasajero, up_hijo, *costo = n

                borde = 16 if up_pasajero else 1
                posicion_nodo = centrar_en_casilla(inicio)
                dibujar_cuadro(SQUARE_COLOR, posicion_nodo, borde, costo[0] if costo else "")


                for direction in direcciones:
                    tamano_flecha = obtener_tamano_flecha(direction, alpha=ESCALAR)
                    centro_flecha = calcular_posicion_flecha(posicion_nodo, direction, tamano_flecha[1] if direction in ["arriba", "abajo"] else tamano_flecha[0])
                    pygame.draw.rect(self.display_surface, ARROW_COLOR, pygame.Rect(centro_flecha[0], centro_flecha[1], tamano_flecha[0], tamano_flecha[1]))

                if  ulitma_profundidad:
                    self.arrow_alpha = min(1, (time.time() - self.chat) / self.time_wait) #esto solo toma valores entre 0 - 1, este valor llega de 0 a 1 en 3 segufnods


                if self.arrow_alpha == 1 or ESCALAR == 1:
                    for i, hijo in enumerate(hijos):
                        borde_hijo = 16 if up_hijo[i] else 1
                        posicion_hijo = centrar_en_casilla(hijo)
                        dibujar_cuadro(SQUARE_COLOR_HIJO, posicion_hijo, borde_hijo, costo[1][i] if costo else "")
            

        if self.init_wait == -1:
            return
        
        time_animation = min(1, (time.time() - self.init_wait) / (self.time_wait * 2))

        if time_animation == 1:
            self.arrow_alpha = 0
            self.chat = time.time()
            self.init_wait = time.time()

            self.all_ya = self.all_ya + self.all_expandir[0]
            self.all_expandir.pop(0)
            
            
        if self.all_expandir == []:
            self.init_wait = -1
            self.init_final = time.time()


        else:
            dibujar_nodos(self.all_ya, False)
            dibujar_nodos(self.all_expandir[0], True)



    def camino_final(self):
        if self.init_final == -1:
            return
        
        time_animation = min(1, (time.time() - self.init_final) / (self.time_wait*3))

        if time_animation == 1:
            self.player.iniciar_caminata(self.solucion["path"])
            self.init_final = -1


        for i, n in enumerate(self.solucion["path"]):
            hijo, direccion, *costo = n

            color_mapping = {
                self.motor.start: AZUL,
                self.motor.passenger: VERDE,
                self.motor.goal: VERDE
            }

            SQUARE_COLOR = color_mapping.get(hijo, ROJO)
            ARROW_COLOR = ROJO
            escalar = 1

            posicion_cuadro = centrar_en_casilla(hijo)
            pygame.draw.rect(self.display_surface, SQUARE_COLOR, pygame.Rect(posicion_cuadro[0], posicion_cuadro[1], CUADRADO_SIZE, CUADRADO_SIZE))
            self.crear_texto(str(costo[0]) if costo else "", 24, posicion_cuadro)

            if  direccion:
                tamano_flecha = obtener_tamano_flecha(direccion, alpha=escalar)
                centro_flecha = calcular_posicion_flecha_final(posicion_cuadro, direccion, tamano_flecha[1] if direccion in ["arriba", "abajo"] else tamano_flecha[0])
                pygame.draw.rect(self.display_surface, ARROW_COLOR, pygame.Rect(centro_flecha[0], centro_flecha[1], tamano_flecha[0], tamano_flecha[1 ]))



       

    def run(self):
        if self.mapa == None:
            self.loading_screen()
            return

        self.visible_sprites.custom_draw()
        self.visible_sprites.update()

        self.crear_caminos_arbol()
        self.camino_final()

        #debug(f"{self.player.status} === {self.player.rect} === {self.player.movimiento_actual}")
    


    def create_map(self):
        layout = self.mapa
        graphics = import_folder(path_main + 'graphics/objects')

        llave_nombre = {
            1: ["pasto", "object"],
            3: ["snorlax_dormido", "object"],
            4: ["snorlax_despierto", "object"],
            5: ["pokeball", "passager"],
            6: ["Shroomish", "goal"],
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
                            (x, y),
                            [self.visible_sprites],
                            self.obstacle_sprites, 
                            (TILESIZE, TILESIZE)
                        )
                    
                    else:
                        surf = pygame.transform.scale(graphics[llave_nombre[int(col)][0]], (TILESIZE, TILESIZE))
                        Tile((x,y),
                             [self.visible_sprites,self.obstacle_sprites],
                             llave_nombre[int(col)][1],
                             surf
                        )



    def reiniciar(self):
        self.create_map()
        self.motor = None

        self.all_ya = []
        self.all_expandir = []
        self.solucion = None

        self.init_wait = -1
        self.init_final = -1 
        self.chat = 0 
        self.time_wait = 0.1



    def setMap(self, map):
        self.mapa = map
        self.create_map()
        self.text_alpha = 255






class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup 
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # creating the floor
        self.floor_surf = pygame.transform.scale(pygame.image.load(path_main + "graphics/tilemap/ground.png").convert(), (640, 640))
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))



    def custom_draw(self):
        # dibuja el suelo (escenario fijo)
        self.display_surface.blit(self.floor_surf, self.floor_rect.topleft)

        # Crea una lista de sprites ordenada por la coordenada Y
        sprites_ordenados = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)

        # Dibuja todos los sprites en el orden de la lista
        for sprite in sprites_ordenados:
            #dibujar las areas para debug

            """
            if isinstance(sprite, Player):
                pygame.draw.rect(self.display_surface, ROJO, sprite.hitbox)
                pygame.draw.rect(self.display_surface, (40, 48, 48), sprite.rect)
            
            elif not isinstance(sprite, Player) and sprite.sprite_type == "passager":
                #pygame.draw.rect(self.display_surface, (255, 0, 0), sprite.hitbox)
                pygame.draw.rect(self.display_surface, (40, 48, 48), sprite.rect)
                pygame.draw.rect(self.display_surface, (100, 255, 100), sprite.activacion)
            
            elif not isinstance(sprite, Player) and sprite.sprite_type == "particule":
                pass
            
            else:
                pygame.draw.rect(self.display_surface, (40, 48, 48), sprite.rect)
                pygame.draw.rect(self.display_surface, (100, 255, 100), sprite.activacion)
            """

            # Dibuja la imagen del sprite
            self.display_surface.blit(sprite.image, sprite.rect.topleft)
            


