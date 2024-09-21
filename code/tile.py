import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups)
		self.sprite_type = sprite_type
		self.image = surface
		self.original_image = self.image.copy()  # Guardar la imagen original para no perder calidad al desvanecer
		self.animation = False
		self.alpha = 255  # Nivel de opacidad inicial

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
			# Desvanecer gradualmente la imagen reduciendo el nivel de alpha
			if self.alpha > 0:
				self.alpha -= 5  # Cambia este valor para controlar la velocidad de desvanecimiento
				self.image = self.original_image.copy()  # Reinicia la imagen antes de cambiar la transparencia
				self.image.set_alpha(self.alpha)  # Aplica la transparencia
			else:
				self.kill()  # Elimina el sprite del grupo cuando esté completamente desvanecido

	def update(self):
		self.desaparecer_animation()
