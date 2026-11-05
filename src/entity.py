import pygame
from object_groups import ObjectGroups
from game import render

# Animation class -> currently hardcoded for entities.
class Animation(object):
	def __init__(self, char_type, motion_type, frames, cooldown):

		self.frames = frames # How many frames for this animation
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
	
	def update(self, player):

		# Update image depending on current animation frame
		self.img = self.animation_list[self.frame_index]

		# Check if enough time has passed since last update, and in that case update to next frame.
		if pygame.time.get_ticks() - self.update_time > self.cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		
		# Resets animation if reached end of animation list.
		if self.frame_index >= len(self.animation_list):
			self.frame_index = 0
			player.is_interacting = False

# Enemy class
class Enemy(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, speed, cooldown):

		# Initialize parent class
		super().__init__()
	
		# Animation
		self.animate_idle = Animation(char_type, 'Idle', 3, cooldown)

		# Rectangle size and speed
		self.rect = self.animate_idle.img.get_rect()
		self.rect.center = (x, y)
		self.speed = speed

	def draw(self, screen, camera):
		self.animate_idle.update(self)
		screen.blit(self.animate_idle.img, (self.rect.x - camera.offset_x, self.rect.y))

# Player class
class Player(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, speed, cooldown):
		# Initialize parent class
		super().__init__()
	
		# Animation
		self.animate_idle = Animation(char_type, 'Idle', 3, cooldown)
		self.animate_move = Animation(char_type, 'Move', 2, cooldown)
		self.animate_interact = Animation(char_type, 'Interact', 5, cooldown * 2)

		# Rectangle size and speed
		self.rect = self.animate_idle.img.get_rect()
		self.rect.center = (x, y)
		self.speed = speed
		
		# Moving directions
		self.moving_right = False
		self.moving_left = False
		self.direction = 1 # -1 for left, 1 for right
		self.flip = False

		# Interactions
		self.is_interacting = False
		self.item_to_pick_up = None
		self.item_collision = False

	def draw(self, screen, camera):
		# Blit entity on screen relative to camera position:
	
		# Move image -> flips image depending on if it's moving left or right
		if self.moving_right or self.moving_left:
			self.animate_move.update(self)
			screen.blit(pygame.transform.flip(self.animate_move.img, self.flip, False), (self.rect.x - camera.offset_x, self.rect.y))

		elif self.is_interacting:
			self.animate_interact.update(self)
			screen.blit(self.animate_interact.img, (self.rect.x - camera.offset_x, self.rect.y))

		# Idle image
		else:
			self.animate_idle.update(self)
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
	
	# Function to check if player is colliding with any items
	# Returns the item if any
	def check_item_collision(self, items):
		collisions = pygame.sprite.spritecollide(self, items, False)
		if collisions:
			return collisions[0]

		return None

	# Pauses the game while player interact animation is running.
	# Removes item from rendered and items group, and adds it to inventory.
	def pick_up_item(self, groups, sprites, enemy, screen, camera):
		item = self.check_item_collision(groups.items)

		if not item:
			return

		self.moving_right = False
		self.moving_left = False
		self.is_interacting = True

		while self.is_interacting:
			self.animate_interact.update(self)
			render(groups, sprites, self, enemy, screen, camera, True)

		item.action('pick up', groups)

	def drop_item(self, groups):
		inventory = groups.inventory.sprites()
		if inventory:
			if inventory[0]:
				inventory[0].action('drop', groups)