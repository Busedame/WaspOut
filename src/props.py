import pygame

class Prop(pygame.sprite.Sprite):
	def __init__(self, prop_name, x, y, scalar):
		super().__init__()
		img = pygame.image.load(f'img/Props/{prop_name}.png')
		self.image = pygame.transform.scale(img, (int(img.get_width() * scalar), (int(img.get_height() * scalar))))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
	
	def draw(self, screen, camera):
		# Blits prop on screen relative to camera position
		screen.blit(self.image, (self.rect.x - camera.offset_x, self.rect.y))
