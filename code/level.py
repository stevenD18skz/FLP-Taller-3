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
        self.indice = 0 # Control para llevar registro de hasta que profundidad del arbol imprimir
        self.arrow_alpha = 0

        self.chat = time.time()
        self.init_wait = -1

        
        self.all_ya = []
        self.all_expandidos = []


        self.tiempo_inicio_juego = time.time()
        self.solucion = None




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
        self.all_ya = []
        self.all_expandidos = self.solucion["nodos_expandidos"]

        print(self.solucion["paths"])

        return self.solucion



    def crear_caminos_arbol(self):
        # Definir el tamaño de la casilla, del cuadrado, y las dimensiones de la flecha
        CASILLA_SIZE = 64
        CUADRADO_SIZE = 32
        FLECHA_ANCHO = 16
        FLECHA_ALTO_VERTICAL = 32  # Flecha que apunta hacia arriba o abajo

        ROJO = (255, 0, 0)
        VERDE = (0, 255, 0)
        AZUL = (0, 0, 255)
        AMARILLO = (255, 255, 0)
        

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




        for i, n in enumerate(self.all_ya):
            SQUARE_COLOR = ROJO
            ARROW_COLOR = ROJO
            SQUARE_COLOR_hijo = ROJO
            BORDER_COLOR = VERDE
            escalar = 1

            inicio, hijos, direcciones, up_pasajero = n

        
            grosor_borde = 0 if up_pasajero else 10

            posicion_cuadro = centrar_en_casilla(inicio)
            pygame.draw.rect(self.display_surface, SQUARE_COLOR, pygame.Rect(posicion_cuadro[0], posicion_cuadro[1], CUADRADO_SIZE, CUADRADO_SIZE))# Dibuja el borde del rectángulo
            pygame.draw.rect(self.display_surface, BORDER_COLOR, pygame.Rect(posicion_cuadro[0], posicion_cuadro[1], CUADRADO_SIZE, CUADRADO_SIZE), grosor_borde)

            for direction in direcciones:
                tamano_flecha = obtener_tamano_flecha(direction, alpha=escalar)
                centro_flecha = calcular_posicion_flecha(posicion_cuadro, direction, tamano_flecha[1] if direction in ["arriba", "abajo"] else tamano_flecha[0])
                pygame.draw.rect(self.display_surface, ARROW_COLOR, pygame.Rect(centro_flecha[0], centro_flecha[1], tamano_flecha[0], tamano_flecha[1]))

                
            for hijo in hijos:
                centro_hijo = centrar_en_casilla(hijo)
                pygame.draw.rect(self.display_surface, SQUARE_COLOR_hijo, pygame.Rect(centro_hijo[0], centro_hijo[1], CUADRADO_SIZE, CUADRADO_SIZE))



        for i, n in enumerate(self.all_expandidos[0]):
            SQUARE_COLOR = AZUL
            ARROW_COLOR = AZUL
            SQUARE_COLOR_hijo = AZUL
            ESCALAR = self.arrow_alpha
            
            inicio, hijos, direcciones, up_pasajero = n

            posicion_cuadro = centrar_en_casilla(inicio)
            pygame.draw.rect(self.display_surface, SQUARE_COLOR, pygame.Rect(posicion_cuadro[0], posicion_cuadro[1], CUADRADO_SIZE, CUADRADO_SIZE))

            for direction in direcciones:
                tamano_flecha = obtener_tamano_flecha(direction, alpha=ESCALAR)
                centro_flecha = calcular_posicion_flecha(posicion_cuadro, direction, tamano_flecha[1] if direction in ["arriba", "abajo"] else tamano_flecha[0])
                pygame.draw.rect(self.display_surface, ARROW_COLOR, pygame.Rect(centro_flecha[0], centro_flecha[1], tamano_flecha[0], tamano_flecha[1]))
            

            self.arrow_alpha = min(1, (time.time() - self.chat) / 0.25) #esto solo toma valores entre 0 - 1, este valor llega de 0 a 1 en 3 segufnods
            
            if self.arrow_alpha == 1 or ESCALAR == 1: #cuando el valor es 1 es que ya se compleot de imprimit la flelcha por compelto 
                for hijo in hijos:
                    centro_hijo = centrar_en_casilla(hijo)
                    pygame.draw.rect(self.display_surface, SQUARE_COLOR_hijo, pygame.Rect(centro_hijo[0], centro_hijo[1], CUADRADO_SIZE, CUADRADO_SIZE))
        
        
    
    def camino_final(self):

        # Definir el tamaño de la casilla, del cuadrado, y las dimensiones de la flecha
        CASILLA_SIZE = 64
        CUADRADO_SIZE = 32
        FLECHA_ANCHO = 16
        FLECHA_ALTO_VERTICAL = 32  # Flecha que apunta hacia arriba o abajo

        ROJO = (255, 0, 0)
        VERDE = (0, 255, 0)
        AZUL = (0, 0, 255)
        AMARILLO = (255, 255, 0)
        

        # Función para calcular la posición central de una casilla
        def centrar_en_casilla(coordenadas):
            y, x = coordenadas
            transformacion = (x * CASILLA_SIZE, y * CASILLA_SIZE)
            centro = (transformacion[0] + CASILLA_SIZE // 2 - CUADRADO_SIZE // 2,
                    transformacion[1] + CASILLA_SIZE // 2 - CUADRADO_SIZE // 2)
            return centro


        # Función para calcular la posición de la flecha
        def calcular_posicion_flecha(centro, direccion, tamano_flecha):
            if direccion == "abajo":
                return (centro[0] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2, centro[1] - tamano_flecha)
            elif direccion == "arriba":
                return (centro[0] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2, centro[1] + CUADRADO_SIZE)
            elif direccion == "derecha":
                return (centro[0] - tamano_flecha, centro[1] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2)
            elif direccion == "izquierda":
                return (centro[0] + CUADRADO_SIZE, centro[1] + CUADRADO_SIZE // 2 - FLECHA_ANCHO // 2)


        # Función para obtener el tamaño de la flecha según la dirección
        def obtener_tamano_flecha(direccion, alpha):
            if direccion == "abajo" or direccion == "arriba":
                return (FLECHA_ANCHO, int(FLECHA_ALTO_VERTICAL*alpha))     #(ancho, alto)
            elif direccion == "derecha" or direccion == "izquierda":
                return (int(FLECHA_ALTO_VERTICAL*alpha), FLECHA_ANCHO)
            
        



        for i, n in enumerate(self.solucion["paths"]):
            SQUARE_COLOR = ROJO
            ARROW_COLOR = ROJO
            SQUARE_COLOR_hijo = ROJO
            BORDER_COLOR = VERDE
            escalar = 1

            #((3, 0), 'abajo')
            hijo, direccion = n

            posicion_cuadro = centrar_en_casilla(hijo)
            pygame.draw.rect(self.display_surface, SQUARE_COLOR, pygame.Rect(posicion_cuadro[0], posicion_cuadro[1], CUADRADO_SIZE, CUADRADO_SIZE))


            tamano_flecha = obtener_tamano_flecha(direccion, alpha=escalar)
            centro_flecha = calcular_posicion_flecha(posicion_cuadro, direccion, tamano_flecha[1] if direccion in ["arriba", "abajo"] else tamano_flecha[0])
            pygame.draw.rect(self.display_surface, ARROW_COLOR, pygame.Rect(centro_flecha[0], centro_flecha[1], tamano_flecha[0], tamano_flecha[1]))

                


        







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





        if not self.init_wait == -1:
            time_animation = min(1, (time.time() - self.init_wait) / 0.4)#este tiempor es el timepor de la animacion de expandir un nodo, llega de 0 - 1 en 5 segundos

            if time_animation == 1:#si ya es 1 es porque ya termino el timepo de la animcaion
                self.indice += 1 #aumentar un nivel de profundidad
                self.arrow_alpha = 0 #reiniciar el valor para la siguiente flecha

                self.chat = time.time()
                self.init_wait = time.time()

                self.all_ya = self.all_ya + self.all_expandidos[0]
                self.all_expandidos.pop(0)
                self.camino_final()


            if self.all_expandidos == []:
                self.player.movimientos = self.solucion["paths"]
                self.init_wait = -1
                

            else:
                self.crear_caminos_arbol()




        debug(f"{self.player.status} === {self.player.rect} === {self.player.movimiento_actual} === {time.time() - self.tiempo_inicio_juego}")
    


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
            


