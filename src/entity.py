import pygame
from object_groups import ObjectGroups
from animation import Animation

# Player class
class Player(pygame.sprite.Sprite):
	inventory: pygame.sprite.Group
	groups: ObjectGroups

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
		self.capturing_enemy = False
		self.releasing_enemy = False
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

	# Moves player rect depending on direction and speed
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

	# Collision checks
	def check_collision(self):

		# Check for item collision
		item = self.check_item_collision(self.groups.items)
		if item:
			self.sprites.interact_box.action(self, 'pick up', item)
			return True
	
		# Check for enemy collision
		enemy = self.check_enemy_collision(self.groups.enemies)
		if enemy:
			self.sprites.interact_box.action(self, 'capture', enemy)
			return True

		return False
	
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
	
	def check_enemy_collision(self, enemies):
		enemy = pygame.sprite.spritecollide(self, enemies, False)
		if not enemy:
			return None
		return enemy[0]

	# Removes item from rendered and items group, and adds it to inventory.
	def pick_up_item(self):
		self.picking_up_item = False

		item = self.check_item_collision(self.groups.items)

		if not item:
			return

		item.action('pick up', self.groups)

		self.capturing_enemy = False

	# Removes item from inventory and adds it to rendered and items group.
	def drop_item(self):
		self.dropping_item = False

		inventory = self.inventory.sprites()

		if not inventory:
			return

		inventory[0].action('drop', self.groups)

		self.releasing_enemy = False
	
	def item_exists_in_inventory(self, name):
		for sprite in self.inventory:
			if sprite.name == name:
				return True

		return False

	def capture(self):
		self.capturing_enemy = False

		enemy = self.check_enemy_collision(self.groups.enemies)
			
		if not enemy:
			return
		
		if not self.item_exists_in_inventory('cup') \
			or not self.item_exists_in_inventory('paper'):
			print('OUCH!')
			return
		
		enemy.action('capture', self.groups)

		self.picking_up_item = False
	
	def release(self):
		self.releasing_enemy = False

		for sprite in self.inventory:
			if isinstance(sprite, Enemy):
				sprite.action('release', self)
				self.dropping_item = False
				return

	def open_window(self, item):
		pass

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

		self.name = char_type

		self.captured = False

	def draw(self, screen, camera):
		if not self.captured:
			self.animate_idle.update(self)
			screen.blit(self.animate_idle.img, (self.rect.x - camera.offset_x, self.rect.y))

	def action(self, action_type, groups):
		if action_type == 'capture':
			self.capture(groups)

		elif action_type == 'release':
			self.release(groups)

	def capture(self, groups):
		self.captured = True
		groups.inventory.add(self)
		groups.rendered.remove(self)
		groups.enemies.remove(self)

		print(f'player captured {self.name}')
	
	def release(self, player):
		self.captured = False
		self.rect.midbottom = (player.rect.centerx, player.rect.bottom)
		player.groups.inventory.remove(self)
		player.groups.rendered.add(self)
		player.groups.enemies.add(self)

		print(f'player released {self.name}')