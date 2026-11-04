import pygame

class Background(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()

		self.image = pygame.image.load('img/Background/bg.png')
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def draw(self, screen, camera):
		# Blits background on screen relative to camera position
		screen.blit(self.image, (self.rect.x - camera.offset_x, self.rect.y))
