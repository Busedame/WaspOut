import pygame

class Sprite(pygame.sprite.Sprite):
	def __init__(self, image_path, x, y, scalar):
		super().__init__()

		img = pygame.image.load(image_path).convert_alpha()
		self.image = pygame.transform.scale(img, (int(img.get_width() * scalar), (int(img.get_height() * scalar))))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
	
	def draw(self, screen, camera):
		# Blits sprite on screen relative to camera position
		screen.blit(self.image, (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y))
