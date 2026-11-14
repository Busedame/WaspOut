import pygame
from object_groups import ObjectGroups
from animation import Animation
from item import ItemInventory, ItemWindow
import string

# Player class
class Player(pygame.sprite.Sprite):
	inventory: pygame.sprite.Group
	groups: ObjectGroups
	sprites: pygame.sprite.Group

	#
	# ///// PLAYER INIT //////
	#

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
		self.interaction = None
		self.enemy_captured = False


	#
	# ///// PLAYER RENDER //////
	#

	# Draw player animation on screen, depending on player movement
	def draw(self, screen, camera):
		# Blit entity on screen relative to camera position:

		if self.interaction:
			screen.blit(self.animate_interact.img, (self.rect.x - camera.offset_x, self.rect.y))
	
		# Move image -> flips image depending on if it's moving left or right
		if self.moving_right or self.moving_left:
			self.animate_move.update()
			screen.blit(pygame.transform.flip(self.animate_move.img, self.flip, False), (self.rect.x - camera.offset_x, self.rect.y))

		# Idle image
		else:
			self.animate_idle.update()
			screen.blit(self.animate_idle.img, (self.rect.x - camera.offset_x, self.rect.y))


	#
	# ///// PLAYER MOVEMENT //////
	#

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


	#
	# ///// COLLISIONS //////
	#

	# Checks if player is colliding with an enemy or an item
	def check_collision(self):

		# Check for window collision
		window_item = self.check_item_collision(self.groups.items)
		if window_item:
			if isinstance(window_item, ItemWindow):
				self.sprites.interact_box.action(self, 'window', window_item)
				return window_item

		# Check for item collision
		item = self.check_item_collision(self.groups.items)
		if item:
			self.sprites.interact_box.action(self, 'pick up', item)
			return item
	
		# Check for enemy collision
		enemy = self.check_enemy_collision(self.groups.enemies)
		if enemy:
			if self.item_exists_in_inventory('cup') and self.item_exists_in_inventory('paper'):
				self.sprites.interact_box.action(self, 'capture', enemy)
				return enemy

		return None
	
	# Checks if player is colliding with an item
	# Returns the smallest rectangle item, if any
	def check_item_collision(self, items):
		collisions = pygame.sprite.spritecollide(self, items, False)
		if not collisions:
			return None
		
		smallest_item = collisions[0]
		for item in collisions:
			if item.rect.w * item.rect.h < smallest_item.rect.w * smallest_item.rect.h:
				smallest_item = item

		return smallest_item
	
	# Checks if player is colliding with an enemy
	# If multiple, returns first one
	def check_enemy_collision(self, enemies):
		enemy = pygame.sprite.spritecollide(self, enemies, False)
		if not enemy:
			return None
		return enemy[0]


	#
	# ///// PLAYER INTERACTIONS //////
	#	

	def handle_interaction(self, target):
		
		# interact == pick up, capture, open
		if self.interaction == 'interact':

			if isinstance(target, ItemWindow):
				target.action('open', self.groups)

			elif isinstance(target, ItemInventory):
				target.action('pick up', self.groups)
			
			elif isinstance(target, Enemy):
				if not self.item_exists_in_inventory('cup') \
				or not self.item_exists_in_inventory('paper'):
					print('OUCH!')
					return

				target.action('capture', self.groups)
				self.enemy_captured = True

			else:
				return

		# inventory == drop, release, close
		elif self.interaction == 'inventory':
			
			if isinstance(target, ItemWindow) and target.opened:
				for sprite in self.inventory:

					if isinstance(sprite, Enemy):
						sprite.action('release', self)
						self.enemy_captured = False
						return
			
			if isinstance(target, ItemWindow):
				target.action('close', self.groups)
				return

			for sprite in self.inventory:

				if isinstance(sprite, ItemInventory):
					sprite.action('drop', self.groups)
					return


	#
	# ///// HELPER FUNCTIONS //////
	#

	# Checks if name exists in inventory, return boolean
	def item_exists_in_inventory(self, name: string):
		for sprite in self.inventory:
			if sprite.name == name:
				return True

		return False



# Enemy class
class Enemy(pygame.sprite.Sprite):
	enemy_count = 0 # For naming enemies: Enemy_1, Enemy_2 etc.

	#
	# ///// ENEMY INIT //////
	#

	def __init__(self, char_type, x, y, speed, cooldown):

		# Initialize parent class
		super().__init__()
	
		# Enemy count
		Enemy.enemy_count += 1
	
		# Animation
		self.animate_idle = Animation(char_type, 'Idle', 3, cooldown)

		# Image
		self.image = self.animate_idle.img

		# Rectangle size and speed
		self.rect = self.animate_idle.img.get_rect()
		self.rect.center = (x, y)
		self.speed = speed

		# Enemy name -> increments by 1 per enemy
		self.name = f"{char_type}_{Enemy.enemy_count}"

		# Boolean indicating if enemy has been captured
		self.captured = False


	#
	# ///// ENEMY RENDER //////
	#

	def draw(self, screen, camera):
		if not self.captured:
			self.animate_idle.update()
			screen.blit(self.animate_idle.img, (self.rect.x - camera.offset_x, self.rect.y))


	#
	# ///// ENEMY ACTIONS //////
	#

	# Calls correct action
	def action(self, action_type, groups):
		if action_type == 'capture':
			self.capture(groups)

		elif action_type == 'release':
			self.release(groups)

	# Handles when enemy is captured
	def capture(self, groups):
		self.captured = True
		groups.inventory.add(self)
		groups.rendered.remove(self)
		groups.enemies.remove(self)

		print(f'player captured {self.name}')
	
	# Handles when enemy is released through window
	def release(self, player):
		player.groups.inventory.remove(self)

		print(f'player released {self.name}')