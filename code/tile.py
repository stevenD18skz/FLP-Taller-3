import random
import pygame
from settings import *
from support import *

class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups)
		self.auxiliar = groups
		self.sprite_type = sprite_type
		self.image = surface
		self.original_image = self.image.copy()  # Guardar la imagen original para no perder calidad al desvanecer
		self.animation = False
		self.alpha = 255  # Nivel de opacidad inicial

		self.frames = {
			'aura': import_folder_un(path_main + 'graphics/particles/aura'),
			'heal': import_folder_un(path_main + 'graphics/particles/heal'),
			'fire': import_folder_un(path_main + 'graphics/particles/fire'),
			'nova': import_folder_un(path_main + 'graphics/particles/nova'),
		}
		
		
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
			self.hitbox = self.rect.inflate(0, 0)
			self.activacion = self.rect.inflate(-TILESIZE, -TILESIZE)
			self.particule = None

		elif sprite_type == 'passager':
			self.rect = self.image.get_rect(topleft=pos)
			self.activacion = self.rect.inflate(-20, -30)
			self.hitbox = self.rect.inflate(0, 0)
			self.particule = Particle(self.rect.center, groups, self.frames['aura'])

		elif sprite_type == 'goal':
			self.rect = self.image.get_rect(topleft=pos)
			self.activacion = self.rect.inflate(-40, -40)
			self.hitbox = self.rect.inflate(0, 0)
			self.particule = Particle(self.rect.center, groups, self.frames['nova'])




	def desaparecer_animation(self):
		if self.animation:
			# Desvanecer gradualmente la imagen
			if self.alpha > 0:
				self.alpha -= 5
				self.image = self.original_image.copy()
				self.image.set_alpha(self.alpha)
			else:
				self.particule.kill()
				self.kill()  # Eliminar el sprite del grupo cuando esté completamente desvanecido


	def update(self):
		print("hola")
		self.desaparecer_animation()

		try:
			self.particule.exist = True
		
		except:
			pass
			




class Particle(pygame.sprite.Sprite):
	def __init__(self, pos, groups, frames):
		super().__init__(groups)
		self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * 2  # Velocidad en dirección aleatoria
		self.sprite_type = "particule"

		self.life = 100  # Duración de la partícula
		self.alpha = 255  # Transparencia inicial
		self.exist = False

		self.frame_index = 0
		self.animation_speed = 0.1
		self.frames = frames
		self.image = self.frames[self.frame_index]
		
		self.rect = self.image.get_rect(center=pos)


	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
			#self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self):
		if self.exist:

			# Desvanecer la partícula gradualmente
			self.life -= 1
			if self.life > 0:
				self.alpha -= 0# 255 // self.life  # Reducir el alpha gradualmente
				self.image.set_alpha(self.alpha)
				self.animate()

			else:
				self.life = 30
				self.exist = False
				self.alpha = 255
				#self.kill()  # Eliminar la partícula cuando su vida se acabe



