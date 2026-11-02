import pygame

# Animation class -> currently hardcoded for entities.
class Animation(object):
	def __init__(self, char_type, motion_type, frames, cooldown):

		self.cooldown = cooldown # How long is the cooldown between frame change
		self.update_time = pygame.time.get_ticks() # Keep track on time to check cooldown
		self.animation_list = [] # Stores each animation frame
		self.frame_index = 0 # Current displayed frame

		# Stores all frames in animation list
		for i in range(frames):
			image = pygame.image.load(f'img/Entity/{char_type}/{motion_type}/{i}.png')
			self.animation_list.append(image)
		
		# Initializes image to be first frame of animation list
		self.img = self.animation_list[self.frame_index]
	
	def update(self):

		# Update image depending on current animation frame
		self.img = self.animation_list[self.frame_index]

		# Check if enough time has passed since last update, and in that case update to next frame.
		if pygame.time.get_ticks() - self.update_time > self.cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		
		# Resets animation if reached end of animation list.
		if self.frame_index >= len(self.animation_list):
			self.frame_index = 0

# Player or enemy class
class Entity(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, speed, cooldown):
	
		# Animation
		self.animate_idle = Animation(char_type, 'Idle', 3, cooldown)
		self.animate_move = Animation(char_type, 'Move', 2, cooldown)

		# Rectangle size and speed
		self.rect = self.animate_idle.img.get_rect()
		self.rect.center = (x, y)
		self.speed = speed

		# Moving directions
		self.moving_right = False
		self.moving_left = False
		self.direction = 1 # -1 for left, 1 for right
		self.flip = False

	def draw(self, screen, camera):

		# Update animations
		self.animate_idle.update()
		self.animate_move.update()

		# Blit entity on screen relative to camera position:
	
		# Move image -> flips image depending on if it's moving left or right
		if self.moving_right or self.moving_left:
			screen.blit(pygame.transform.flip(self.animate_move.img, self.flip, False), (self.rect.x - camera.offset_x, self.rect.y))
	
		# Idle image
		else:
			screen.blit(self.animate_idle.img, (self.rect.x - camera.offset_x, self.rect.y))


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