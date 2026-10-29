import pygame

class Props(object):
	def __init__(self, prop_type, x, y, scalar):
		image = pygame.image.load(f'img/Props/{prop_type}.png')
		self.img = pygame.transform.scale(image, (int(image.get_width() * scalar), (int(image.get_height() * scalar))))
		self.rect = self.img.get_rect()
		self.rect.center = (x, y)
	
	def draw(self, screen):
		screen.blit(self.img, self.rect)