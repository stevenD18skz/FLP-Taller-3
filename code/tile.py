import random
import pygame
from settings import *
from support import *

class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups)
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

		
		self.auxiliar = groups
		
		
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
			self.hitbox = self.rect.inflate(0, 0)
			self.activacion = self.rect.inflate(-TILESIZE, -TILESIZE)

		elif sprite_type == 'passager':
			self.rect = self.image.get_rect(topleft=pos)
			self.activacion = self.rect.inflate(-20, -30)
			self.hitbox = self.rect.inflate(0, 0)
			
		elif sprite_type == 'goal':
			self.rect = self.image.get_rect(topleft=pos)
			self.activacion = self.rect.inflate(-40, -40)
			self.hitbox = self.rect.inflate(0, 0)
		



	def desaparecer_animation(self):
		if self.animation:


			if self.alpha > 0:
				self.alpha -= 5
				self.image = self.original_image.copy()
				self.image.set_alpha(self.alpha)

			else:
				self.kill()
				if self.sprite_type != "object":
					self.particule.kill()



	def update(self):
		self.desaparecer_animation()


	def setAnimation(self, valor):
		self.animation = valor
		
		self.particule = Particle(self.rect.center, self.auxiliar, self.frames['nova'])
		self.particule.exist = True






class Particle(pygame.sprite.Sprite):
	def __init__(self, pos, groups, frames):
		super().__init__(groups)
		self.sprite_type = "particule"
		self.frame_index = 0
		self.animation_speed = 0.02
		self.frames = frames
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center=pos)

		
		self.life = 100  # Duración de la partícula
		self.exist = False


	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.frame_index = 0

		else:
			self.image = self.frames[int(self.frame_index)]



	def update(self):
		if self.exist:
			# Desvanecer la partícula gradualmente
			self.life -= 1
			if self.life > 0:
				self.animate()

			else:
				self.kill()



