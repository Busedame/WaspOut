import pygame

# Class for player and enemies
# __init__ -> initializes the instance
# draw -> blits the character on screen
# move -> moves the character's x position

class Entity(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, speed):
		self.img = pygame.image.load(f'img/Entity/{char_type}/Idle/0.png')
		self.rect = self.img.get_rect()
		self.rect.center = (x, y)
		self.speed = speed

		# Moving directions
		self.moving_right = False
		self.moving_left = False
		self.direction = 1 # -1 for left, 1 for right
		self.flip = False
	
	def draw(self, screen, camera):
		# Blits entity on screen relative to camera position
		# Flips image depending on if it's moving left or right
		screen.blit(pygame.transform.flip(self.img, self.flip, False), (self.rect.x - camera.offset_x, self.rect.y))

	def move(self):
		dx = 0

		if self.moving_left:
			dx = self.speed
			self.flip = False
			self.direction = -1
	
		if self.moving_right:
			dx = self.speed
			self.flip = True
			self.direction = 1

		# Updates player world position
		self.rect.x += dx * self.direction

		# Blocks player from moving out of screen
		self.rect.x = max(0, min(self.rect.x, 1280 - self.rect.w))