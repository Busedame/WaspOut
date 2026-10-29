import pygame

class Background(object):
	def __init__(self, x, y):
		self.img = pygame.image.load('img/Background/bg.png')
		self.rect = self.img.get_rect()
		self.rect.center = (x, y)

	def draw(self, screen):
		screen.blit(self.img, self.rect)
