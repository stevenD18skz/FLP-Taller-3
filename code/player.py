import pygame
from settings import *
from debug import *
from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, size):
        super().__init__(groups)
        # Graphics display
        self.original_size = size
        self.image = pygame.transform.scale(pygame.image.load(path_main + 'graphics/objects/lapras.png').convert_alpha(), size)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)


        # graphics animation
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0

        # Movimiento
        self.in_movimiento = False
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8 #velocidad tiene que ser en potencia de 2
        self.obstacle_sprites = obstacle_sprites
        self.movimientos = []
        self.movimiento_actual = None
        self.meta_pos = list(self.hitbox[:2])

        # Animación de inicio
        self.is_starting = False  # Estado de animación inicial
        self.scale_factor = 1.0  # Factor de escalado
        self.scale_count = 0.01
    



    def import_player_assets(self):
        character_path = path_main + 'graphics/player/'
        self.animations = {'up': [],'down': [],'left': [],'right': [],
            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_jump':[],'left_jump':[],'up_jump':[],'down_jump':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = list(map(lambda x: pygame.transform.scale(x, (64, 64)), import_folder_un(full_path)))




    def start_animation(self):
        """Animación inicial que escala el sprite hacia arriba y luego lo vuelve a su tamaño original."""

        # Aumentar el tamaño del sprite
        self.scale_factor += self.scale_count

        # Escalar la imagen
        new_size = (int(self.original_size[0] * self.scale_factor), int(self.original_size[1] * self.scale_factor))
        self.image = pygame.transform.scale(pygame.image.load(path_main + 'graphics/objects/lapras.png').convert_alpha(), new_size)

        # Actualizar la posición del rectángulo para que el sprite permanezca centrado
        self.rect = self.image.get_rect(center=self.rect.center)
        self.hitbox = self.rect.inflate(0, 0)

        # Volver al tamaño original después de alcanzar el tamaño máximo
        if self.scale_factor >= 1.5:
            self.scale_count = self.scale_count * -1


        elif self.scale_factor <= 1:
            self.is_starting = False  # Fin de la animación de inicio
            self.scale_factor = 1.0  # Resetear el factor de escala

            # Restablecer el tamaño original del sprite
            self.image = pygame.transform.scale(pygame.image.load(path_main + 'graphics/objects/lapras.png').convert_alpha(), self.original_size)
            self.rect = self.save_pos_b
            self.hitbox = self.rect.inflate(0, 0)





    def input(self):
        if self.is_starting:
            return

        if self.movimientos != []:
            # Tomar el siguiente movimiento de la lista
            self.movimiento_actual = self.movimientos[0][1]

            if self.movimiento_actual.lower() in ['left', "izquierda"]:
                self.status = 'left'
                self.direction.x = -1
                self.direction.y = 0
            elif self.movimiento_actual.lower() in ['right', "derecha"]:
                self.status = 'right'
                self.direction.x = 1
                self.direction.y = 0
            elif self.movimiento_actual.lower() in ['up', "arriba"]:
                self.status = 'up'
                self.direction.x = 0
                self.direction.y = -1
            elif self.movimiento_actual.lower() in ['down', "abajo"]:
                self.status = 'down'
                self.direction.x = 0
                self.direction.y = 1

            # Comenzar movimiento
            self.in_movimiento = True
            self.meta_pos = self.movimientos[0][0][::-1]
        
        else:
            self.status = 'down_idle'
            


    def iniciar_caminata(self, camino):
        self.movimientos = camino
        self.is_starting = True
        self.save_pos_b = self.rect




    def movimiento_caminata(self):
        current_pos = list(map(lambda x: x / TILESIZE, list(self.rect[:2])))  # traducir las (x,y) a cordenadas normales (128, 64) ==> (2,1)

        if self.in_movimiento:
            if [a - b for a, b in zip(current_pos, self.meta_pos)] == [0.0, 0.0]:  # ya se completó la animación del personaje avanzando
                self.in_movimiento = False
                self.movimientos.pop(0)
                self.movimiento_actual = None
                self.direction.x = 0
                self.direction.y = 0

            else:
                self.rect.x += self.direction.x * self.speed
                self.rect.y += self.direction.y * self.speed
                self.hitbox = self.rect
                self.collision()
                



    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index 
        self.frame_index += 0.15
        if self.frame_index > len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)




    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'



    def collision(self):
        for sprite in self.obstacle_sprites:
            if sprite.sprite_type == "particule":
                pass

            elif sprite.activacion.colliderect(self.hitbox):
                print("llegue a una meta" + sprite.sprite_type)
                sprite.animation = True
                sprite.activacion.width = 0
                sprite.activacion.height = 0

          

    def update(self):
        if self.is_starting:
            self.start_animation()
            return
        
        self.get_status()
        self.animate()
        self.input()
        self.movimiento_caminata()
