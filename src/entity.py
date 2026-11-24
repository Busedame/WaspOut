import pygame
from object_groups import ObjectGroups
from animation import Animation
from item import ItemInventory, ItemWindow
import string
import random
from sound import Sound
import math

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
		self.animate_climb = Animation(char_type, 'Climb', 2, cooldown)

		# Rectangle size and speed
		self.rect = self.animate_idle.img.get_rect()
		self.rect.center = (x, y)
		self.speed = speed

		# y coordinates restrictions
		# Unless player is in ladder, it can ONLY move sideways if it is one of these two y values.
		self.min_y = 200 # Minimum player y coordinate
		self.max_y = 680 # Maximum player y coordinate
		
		# Moving directions
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False
		self.x_direction = 1 # -1 for left, 1 for right
		self.y_direction = 1 # 1 for down, -1 for up
		self.flip = False

		# Interactions
		self.interaction = None
		self.enemy_captured = False

		# How many enemies are captured
		self.score = 0

		# Selected item from inventory
		self.selected_item = None

	#
	# ///// PLAYER RENDER //////
	#

	# Draw player animation on screen, depending on player movement
	def draw(self, screen, camera):
		# Blit entity on screen relative to camera position:

		#if self.interaction:
		#	screen.blit(self.animate_interact.img, (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y))
		
		# Climb image
		if self.using_ladder():
			if self.moving_up or self.moving_down:
				self.animate_climb.update()
			screen.blit(self.animate_climb.img, (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y))
	
		# Move image -> flips image depending on if it's moving left or right
		elif self.moving_right or self.moving_left:
			self.animate_move.update()
			screen.blit(pygame.transform.flip(self.animate_move.img, self.flip, False), (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y))

		# Idle image
		else:
			self.animate_idle.update()
			screen.blit(self.animate_idle.img, (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y))


	#
	# ///// PLAYER MOVEMENT //////
	#

	# Moves player rect depending on direction and speed
	def move(self, world_width, dt):
		dx = 0
		dy = 0

		if self.rect.y == self.min_y or self.rect.y == self.max_y:
			if self.moving_left:
				dx = self.speed
				self.flip = False
				self.x_direction = -1

			if self.moving_right:
				dx = self.speed
				self.flip = True
				self.x_direction = 1

			# Updates player world position
			self.rect.x += dx * (60 * dt) * self.x_direction # Velocity

			# Blocks player from moving out of world
			if self.rect.y == self.min_y:
				self.rect.x = max(0, min(self.rect.x, world_width - 400 - self.rect.w)) # Hardcoded to cut off background on right side only upstairs
			else:
				self.rect.x = max(0, min(self.rect.x, world_width - self.rect.w))
		
		if self.check_ladder_collision():
			if self.moving_up:
				dy = self.speed
				self.y_direction = -1

			if self.moving_down:
				dy = self.speed
				self.y_direction = 1
			
			self.rect.y += dy * self.y_direction # Velocity
			self.rect.y = max(self.min_y, min(self.rect.y, self.max_y))


	#
	# ///// COLLISIONS //////
	#

	# Checks if player is colliding with an enemy or an item
	def check_collision(self):

		# Check for enemy collision
		enemy = self.check_enemy_collision(self.groups.enemies)
		if enemy:
			if self.item_exists_in_inventory('glass') and self.item_exists_in_inventory('paper'):
				self.sprites.interact_box.action(self, 'capture', enemy)
				return enemy

		# Check for item collision
		item = self.check_item_collision(self.groups.items)

		if item:

			# Check for inventory item collision
			if isinstance(item, ItemInventory):
				self.sprites.interact_box.action(self, 'pick up', item)
				return item
	
			# Check for window collision
			elif isinstance(item, ItemWindow):
				self.sprites.interact_box.action(self, 'window', item)
				return item

		return None

	def check_ladder_collision(self):

		ladder = self.sprites.ladder.hitbox
		
		# Going upstairs -> checks if middle of player rect intersects with ladder's hitbox.
		if ladder.collidepoint(self.rect.centerx, self.rect.centery):
			return True
		
		# Going downstairs -> checks if bottom of player rect intersects with ladder's hitbox.
		elif ladder.collidepoint(self.rect.centerx, self.rect.bottom):
			return True

		return False

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
		
		if self.using_ladder():
			return

		# Select an item from inventory
		if isinstance(self.interaction, int):
			for item in self.inventory:
				if item.index == self.interaction:
					item.select_from_inventory()
					self.selected_item = item
					break

		if self.interaction == 'deselect':
			if self.selected_item == None:
				return
			self.selected_item.deselect_from_inventory()
			self.selected_item = None

		# interact == pick up, capture, open/close window
		elif self.interaction == 'interact':

			if isinstance(target, ItemWindow):
				target.action(self.groups)

			elif isinstance(target, ItemInventory):
				target.action('pick up', self.groups)
			
			elif isinstance(target, Enemy):
				if not self.item_exists_in_inventory('glass') \
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

			for sprite in self.inventory:

				if isinstance(sprite, ItemInventory):
					if not self.enemy_captured:
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
	
	def using_ladder(self):
		if self.rect.y == self.min_y or self.rect.y == self.max_y:
			return False
		return True


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
		self.animate_move = Animation(char_type, 'Move', 3, cooldown)

		# Image
		self.image = self.animate_move.img

		# Possible spawn locations
		self.enemy_x_locations = range(50, 1370) # Hardset to fit into CURRENT WORLD DIMENSIONS.
		self.enemy_y_locations = range(200, 350) # Hardset to fit into CURRENT WORLD DIMENSIONS.

		# Rectangle size and speed
		self.rect = self.animate_move.img.get_rect()
		self.rect.center = (random.choice(self.enemy_x_locations), random.choice(self.enemy_y_locations)) # Spawn point
		self.speed = speed

		# Enemy name -> increments by 1 per enemy
		self.name = f"{char_type}_{Enemy.enemy_count}"

		# Boolean indicating if enemy has been captured
		self.captured = False

		# Load and play idle sound file
		self.idle_sound = Sound('wasp.wav').sound
		self.idle_sound.play(-1)
		self.idle_sound.set_volume(0)

		# Load additional sound files
		self.captured_sound = Sound('wasp_caught.wav').sound
		self.released_sound = Sound('wasp_release.wav').sound

		# Start position and velocity
		self.pos = pygame.math.Vector2(self.rect.center) # Start position stored in a Vector2
		self.velocity = pygame.math.Vector2(self.speed, 0).rotate(random.uniform(0, 360)) # Speed and direction (direction initialized to random angle)
	
	#
	# ///// ENEMY RENDER //////
	#

	def draw(self, screen, camera):
		if not self.captured:
			self.animate_move.update()
			screen.blit(self.animate_move.img, (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y))

	#
	# ///// ENEMY ACTIONS //////
	#

	# Adjusts the volume of wasp idle sound, depending on how close it is to player.
	def adjust_idle_sound(self, player):
		if self.captured:
			return

		max_distance_x = 600.0
		max_distance_y = 400.0

		# abs() gives the difference between the two points but seen as the distance from 0.
		distance_x = abs(self.rect.centerx - player.rect.centerx)
		distance_y = abs(self.rect.centery - player.rect.centery)

		# Using Pythagoras to get the correct distance, since both x and y axis must be considered.
		# Normalize by dividing by max distance: e.g. 300 / 600 = 0.5.
		normalized_distance = math.sqrt(
			(distance_x / max_distance_x) ** 2 +
			(distance_y / max_distance_y) ** 2
		)
	
		# If player is upstairs and close enough to wasp -> play sound at correct volume.
		if player.rect.y != player.max_y and normalized_distance <= 1.0:
			volume = 1.0 - normalized_distance
			self.idle_sound.set_volume(volume)
		else:
			self.idle_sound.set_volume(0.0)

	# Moving algorithm to move wasp semi-random.
	def move(self):

		# Rotate the move direction by a random value between -10 and 10 degrees.
		self.velocity.rotate_ip(random.uniform(-10, 10))
		self.pos += self.velocity

		# Keep wasp inside world by changing direction at the edges.
		if self.pos.x < 50 or self.pos.x > 1370:
			self.velocity.x *= -1
			self.pos.x = max(50, min(1370, self.pos.x))

		if self.pos.y < 100 or self.pos.y > 350:
			self.velocity.y *= -1
			self.pos.y = max(100, min(350, self.pos.y))

		self.rect.center = (round(self.pos.x), round(self.pos.y))

	# Calls correct action
	def action(self, action_type, groups):
		if action_type == 'capture':
			self.capture(groups)

		elif action_type == 'release':
			self.release(groups)

	# Handles when enemy is captured
	def capture(self, groups):

		# Debug print
		print(f'player captured {self.name}')

		# Update enemy state
		self.captured = True
		
		# Add to inventory
		groups.inventory.add(self)

		# Remove from groups
		groups.rendered.remove(self)
		groups.enemies.remove(self) # Needs to change at some point =)

		# Temp sound
		self.idle_sound.stop()
		self.captured_sound.play(-1)
	
	# Handles when enemy is released through window
	def release(self, player):

		# Debug print
		print(f'player released {self.name}')

		# Remove from inventory
		player.groups.inventory.remove(self)

		# Respawn
		self.rect.center = (random.choice(self.enemy_x_locations), random.choice(self.enemy_y_locations))

		# Update enemy state
		self.captured = False

		# Re-add to groups
		player.groups.rendered.add(self)
		player.groups.enemies.add(self)

		# Change sound
		self.captured_sound.stop()
		self.idle_sound.play(-1)
		self.released_sound.play(0)

		# Add to player score
		player.score += 1