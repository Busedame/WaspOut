import pygame
from objects import Sprites, Entities
from object_groups import ObjectGroups
from camera import Camera
from debug import debug

DEBUG = False

class Game():
	def __init__(self):
		# Window width and height
		self.window_width = 640
		self.window_height = 480

		# Window init and settings
		self.screen = pygame.display.set_mode((self.window_width, self.window_height))
		pygame.display.set_caption('Wasp out!')

		# Initialize world
		self.entities = Entities(self.window_width, self.window_height)
		self.sprites = Sprites(self.window_width, self.window_height, self.entities.player)

		# Initialize groups
		self.groups = ObjectGroups(self.sprites, self.entities)

		# Reassign player and enemy to separate variables for easier accessibility
		self.player = self.entities.player
		self.enemy = self.entities.enemy

		# Initialize camera
		self.camera = Camera(0, 0, self.window_width, self.window_height, self.player)

		# Collision boolean (True if player is colliding with enemy or item)
		self.collision = False

		# Loop booleans
		self.intro = True
		self.running = True

		# Framerate calculation
		self.dt = 0
		self.clock = pygame.time.Clock()

	# Game intro loop
	def intro_loop(self):
		while self.intro:

			# Draw all intro images
			self.groups.draw(self.screen, self.camera, self.groups.intro)

			# Render all intro images
			pygame.display.flip()

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.intro = False
						self.running = False
					if event.key == pygame.K_SPACE:
						self.intro = False
	
			# Caps the runtime speed to not kill CPU
			self.clock.tick(60)

	# Game main loop
	def main_loop(self):

		while self.running:
			self.update()
			self.render()

			# Check for events
			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					self.running = False
		
				# Player actions
				if event.type == pygame.KEYDOWN:
					# Picking up item
					if event.key == pygame.K_w:
						self.player.picking_up_item = True
						self.player.capturing_enemy = True
					elif event.key == pygame.K_s:
						self.player.dropping_item = True
						self.player.releasing_enemy = True
					# Moving right
					elif event.key == pygame.K_d:
						self.player.moving_right = True
					# Moving left
					elif event.key == pygame.K_a:
						self.player.moving_left = True
					# Exit game
					if event.key == pygame.K_ESCAPE:
						self.running = False

				if event.type == pygame.KEYUP:
					if event.key == pygame.K_d:
						self.player.moving_right = False
					if event.key == pygame.K_a:
						self.player.moving_left = False
					elif event.key == pygame.K_s:
						self.player.dropping_item = False

			# Get delta time
			self.dt = self.clock.tick(60) / 1000

			if DEBUG:
				debug(self.entities, self.sprites, self.camera)

	# Game update current state
	def update(self):

		# Move the player
		if self.player.moving_right or self.player.moving_left:
			self.player.move()
	
		# Player interacts
		if self.player.picking_up_item:
			self.player.pick_up_item()

		if self.player.capturing_enemy:
			self.player.capture()

		if self.player.releasing_enemy:
			self.player.release()

		if self.player.dropping_item:
			self.player.drop_item()

		# Move the camera
		self.camera.move()

		self.collision = self.player.check_collision()

	# Game render current state
	def render(self):

		# Draw background, items and props
		self.groups.draw(self.screen, self.camera, self.groups.rendered)

		# Draw the enemy
		self.enemy.draw(self.screen, self.camera)

		# Draw the player
		self.player.draw(self.screen, self.camera)

		# Draw interact_box if any
		if self.collision:
			self.sprites.interact_box.draw(self.screen, self.camera)

		# Render all images
		pygame.display.flip()