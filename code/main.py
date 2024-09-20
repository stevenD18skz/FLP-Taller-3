import pygame, sys
from settings import *
from level import Level
from player import *



class Game:
	def __init__(self):
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('POKEMON')
		self.clock = pygame.time.Clock()
		self.level = Level()


	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.MOUSEMOTION:
					x, y = pygame.mouse.get_pos()
					#print(f"Posición del ratón: 222222 ({x}, {y})")

				elif event.type == pygame.MOUSEBUTTONDOWN:
					x, y = pygame.mouse.get_pos()
					#print(f"Posición del ratón:34444444 ({x}, {y})")



			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)
			



if __name__ == '__main__':
	game = Game()
	game.run()

