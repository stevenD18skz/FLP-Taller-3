import time
import pygame 
from settings import *
from tile import Tile
from debug import debug
from support import *
from player import Player

from Logic.BusquedaAmplitud import BusquedaAmplitud
from Logic.BusquedaCosto import BusquedaCosto
from Logic.BusquedaProfundidad import BusquedaProfundidad


class Level:
    def __init__(self):
        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.caminos = pygame.sprite.Group()

        self.mapa = None
        self.motor = None

        # Variables para la animación de texto
        self.text_alpha = 255  # Opacidad inicial
        self.fade_speed = 5    # Velocidad de desvanecimiento
        self.fading_out = True  # Control de la animación de desvanecimiento



        #variables control de timepo
        self.arrow_alpha = 0

        self.all_ya = []
        self.all_expandidos = []
        self.solucion = None

        self.chat = 0 #Manejador de tiempo para  "arrow_alpha"
        self.init_wait = -1 #Manejador de tiempo para la animaciones
        self.init_final = -1



    def loading_screen(self):
        screen_width = 640
        screen_height = 640

        # Colores
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        
        # Fuente
        font = pygame.font.Font(None, 50)

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



    def ejecutarAlgoritmo(self, eleccion):
        algoritmos = {
            "Amplitud": BusquedaAmplitud,
            "Costo uniforme": BusquedaCosto,
            "Profundidad evitando ciclos": BusquedaProfundidad,
            "Avara": None,
            "A*": None,
        }

        motor = algoritmos[eleccion](self.mapa)
        self.solucion = motor.solucionar()

        self.init_wait = time.time()
        self.chat = time.time()
        self.all_expandidos = self.solucion["nodos_expandidos"]

        return self.solucion



    def crear_caminos_arbol(self):

        def dibujar_nodos(ln, ulitma_profundidad):
            for i, n in enumerate(ln):
                #si ultima_profundidad es false entonces son los ya expandidos(rojos), si es true (blue)
                SQUARE_COLOR = ROJO if not ulitma_profundidad else AZUL
                ARROW_COLOR = ROJO if not ulitma_profundidad else AZUL
                SQUARE_COLOR_HIJO = ROJO if not ulitma_profundidad else AZUL
                ESCALAR = 1  if not ulitma_profundidad else self.arrow_alpha

                inicio, hijos, direcciones, up_pasajero = n

                grosor_borde = 0 if up_pasajero else 10
                BORDER_COLOR = VERDE

                posicion_cuadro = centrar_en_casilla(inicio)
                pygame.draw.rect(self.display_surface, SQUARE_COLOR, pygame.Rect(posicion_cuadro[0], posicion_cuadro[1], CUADRADO_SIZE, CUADRADO_SIZE))
                pygame.draw.rect(self.display_surface, BORDER_COLOR, pygame.Rect(posicion_cuadro[0], posicion_cuadro[1], CUADRADO_SIZE, CUADRADO_SIZE), grosor_borde)

                for direction in direcciones:
                    tamano_flecha = obtener_tamano_flecha(direction, alpha=ESCALAR)
                    centro_flecha = calcular_posicion_flecha(posicion_cuadro, direction, tamano_flecha[1] if direction in ["arriba", "abajo"] else tamano_flecha[0])
                    pygame.draw.rect(self.display_surface, ARROW_COLOR, pygame.Rect(centro_flecha[0], centro_flecha[1], tamano_flecha[0], tamano_flecha[1]))


                if  ulitma_profundidad:
                    self.arrow_alpha = min(1, (time.time() - self.chat) / 0.1) #esto solo toma valores entre 0 - 1, este valor llega de 0 a 1 en 3 segufnods


                if self.arrow_alpha == 1 or ESCALAR == 1:
                    for hijo in hijos:
                        centro_hijo = centrar_en_casilla(hijo)
                        pygame.draw.rect(self.display_surface, SQUARE_COLOR_HIJO, pygame.Rect(centro_hijo[0], centro_hijo[1], CUADRADO_SIZE, CUADRADO_SIZE))
            


        if self.init_wait == -1:
            return
        
        time_animation = min(1, (time.time() - self.init_wait) / 0.2)

        if time_animation == 1:
            self.arrow_alpha = 0
            self.chat = time.time()
            self.init_wait = time.time()

            self.all_ya = self.all_ya + self.all_expandidos[0]
            self.all_expandidos.pop(0)


        if self.all_expandidos == []:
            self.init_wait = -1
            self.init_final = time.time()


        else:
            dibujar_nodos(self.all_ya, False)
            dibujar_nodos(self.all_expandidos[0], True)



    def camino_final(self):

        if self.init_final == -1:
            return
        
        time_animation = min(1, (time.time() - self.init_final) / 2)

        if time_animation == 1:
            self.player.movimientos = self.solucion["paths"]
            self.init_final = -1
        


        lista = self.solucion["paths"]

        inicio_d = lista[0][1]

        #if inicio_d == "abajo":
        #    inicio = lista[0][0] - 




        for i, n in enumerate(self.solucion["paths"]):
            SQUARE_COLOR = ROJO
            ARROW_COLOR = ROJO
            escalar = 1

            #((3, 0), 'abajo')
            hijo, direccion = n

            posicion_cuadro = centrar_en_casilla(hijo)
            pygame.draw.rect(self.display_surface, SQUARE_COLOR, pygame.Rect(posicion_cuadro[0], posicion_cuadro[1], CUADRADO_SIZE, CUADRADO_SIZE))


            tamano_flecha = obtener_tamano_flecha(direccion, alpha=escalar)
            centro_flecha = calcular_posicion_flecha_final(posicion_cuadro, direccion, tamano_flecha[1] if direccion in ["arriba", "abajo"] else tamano_flecha[0])
            pygame.draw.rect(self.display_surface, ARROW_COLOR, pygame.Rect(centro_flecha[0], centro_flecha[1], tamano_flecha[0], tamano_flecha[1 ]))

            """
            [((3, 0), 'abajo'), ((4, 0), 'abajo'), ((5, 0), 'abajo'), ((6, 0), 'abajo'), ((5, 0), 'arriba'), ((4, 0), 'arriba'), ((3, 0), 'arriba'), ((3, 1), 'derecha'), ((3, 2), 'derecha'), ((3, 3), 'derecha'), ((3, 4), 'derecha'), ((3, 5), 'derecha'), ((3, 6), 'derecha'), ((3, 7), 'derecha'), ((3, 8), 'derecha'), ((3, 9), 'derecha'), ((4, 9), 'abajo'), ((5, 9), 'abajo')]
            """

       

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



    def run(self):
        if self.mapa == None:
            self.loading_screen()
            return

        self.visible_sprites.custom_draw()
        self.visible_sprites.update()

        self.crear_caminos_arbol()
        self.camino_final()


        debug(f"{self.player.status} === {self.player.rect} === {self.player.movimiento_actual}")
    

    def reiniciar(self):
        self.create_map()
        self.motor = BusquedaAmplitud(self.mapa)
        self.solucion = None
        self.all_expandidos = None
        self.all_ya = None



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
            


