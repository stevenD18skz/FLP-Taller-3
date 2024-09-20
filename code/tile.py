import pygame 
from settings import *



class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
		super().__init__(groups)
		self.sprite_type = sprite_type
		self.image = surface
		
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft = (pos[0], pos[1]))
			self.hitbox = self.rect.inflate(0,0)
			self.activacion = self.rect.inflate(0,0)

		
		elif sprite_type == 'entities':
			#self.image = pygame.transform.scale(surface, (64, 64))

			self.rect = self.image.get_rect(topleft = pos)
			self.activacion = self.rect.inflate(10,10)
			self.hitbox = self.rect.inflate(0, 0)


		else:
			self.rect = self.image.get_rect(topleft = pos)
			self.activacion = self.rect.inflate(0,0)
			self.hitbox = self.rect.inflate(0, 0)

		
		