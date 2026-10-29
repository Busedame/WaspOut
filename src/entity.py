import pygame

# Parent class to all entities -> can be player, enemy or just a static object.
class Entity(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, speed):
		self.img = pygame.image.load(f'img/{char_type}/Idle/0.png')
		self.rect = self.img.get_rect()
		self.rect.center = (x, y)
		self.speed = speed
		self.direction = 1 # -1 for left, 1 for right
		self.flip = False
	
	def draw(self, screen):
		screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)
	
	def move(self, move_right, move_left):
		dx = 0

		if move_left:
			dx = self.speed
			self.flip = False
			self.direction = -1
	
		if move_right:
			dx = self.speed
			self.flip = True
			self.direction = 1

		self.rect.x += dx * self.direction
