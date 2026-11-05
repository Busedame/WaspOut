import pygame
from object_groups import ObjectGroups
from game import render
from animation import Animation

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
		self.picking_up_item = False
		self.dropping_item = False
		#self.is_interacting = False

	def draw(self, screen, camera):
		# Blit entity on screen relative to camera position:
	
		# Move image -> flips image depending on if it's moving left or right
		if self.moving_right or self.moving_left:
			self.animate_move.update(self)
			screen.blit(pygame.transform.flip(self.animate_move.img, self.flip, False), (self.rect.x - camera.offset_x, self.rect.y))

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
		if not collisions:
			return None
		
		smallest_item = collisions[0]
		for item in collisions:
			if item.rect.w * item.rect.h < smallest_item.rect.w * smallest_item.rect.h:
				smallest_item = item

		return smallest_item

	# Pauses the game while player interact animation is running.
	# Removes item from rendered and items group, and adds it to inventory.
	def pick_up_item(self, groups):
		self.picking_up_item = False

		item = self.check_item_collision(groups.items)

		if not item:
			return

		item.action('pick up', groups)

	def drop_item(self, groups):
		self.dropping_item = False

		inventory = groups.inventory.sprites()

		if not inventory:
			return

		inventory[0].action('drop', groups)

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
