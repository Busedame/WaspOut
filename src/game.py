import pygame
from objects import Sprites, Entities
from object_groups import ObjectGroups
from camera import Camera
from debug import debug
from item import ItemLadder

DEBUG = False

class Game():
	def __init__(self):
		# Window width and height
		self.window_width = 640
		self.window_height = 480

		# Window init and settings
		self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN)
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

		# Collision
		self.collision = None # item, enemy or None

		# Loop booleans
		self.intro = True
		self.running = True
		self.outro = True

		# Framerate calculation
		self.dt = 0
		self.clock = pygame.time.Clock()

		surf = pygame.image.load('img/Items/cup.png').convert_alpha()
		#surf = pygame.transform.scale(surf, (32, 32))  # Standard pekerstørrelse
		cursor = pygame.cursors.Cursor((0, 0), surf)  # (0, 0) er klikkpunktet øverst til venstre
		pygame.mouse.set_cursor(cursor)


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

			#if not self.groups.enemies.sprites():
			#	self.end_game()
			#	self.running = False

			# Check for events
			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					self.running = False
		
				# Player actions
				if event.type == pygame.KEYDOWN:
					# Picking up item, capturing enemy or opening window
					if event.key == pygame.K_e:
						self.player.interaction = 'interact'
					# Dropping item, releasing enemy or closing window
					elif event.key == pygame.K_r:
						self.player.interaction = 'inventory'
					# Moving right
					elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
						self.player.moving_right = True
					# Moving left
					elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
						self.player.moving_left = True
					# Moving up
					elif event.key == pygame.K_w or event.key == pygame.K_UP:
						self.player.moving_up = True
					# Moving down
					elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
						self.player.moving_down = True
					# Exit game
					if event.key == pygame.K_ESCAPE:
						self.running = False
				
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						print('Clicked')

				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
						self.player.moving_right = False
					if event.key == pygame.K_a or event.key == pygame.K_LEFT:
						self.player.moving_left = False
					if event.key == pygame.K_w or event.key == pygame.K_UP:
						self.player.moving_up = False
					if event.key == pygame.K_s or event.key == pygame.K_DOWN:
						self.player.moving_down = False

			# Get delta time
			self.dt = self.clock.tick(60) / 1000


			if DEBUG:
				debug(self.entities, self.sprites, self.camera)
				print(self.sprites.inventory.print_items())

	# Game update current state
	def update(self):

		# Update collision -> 'item', 'enemy' or None
		self.collision = self.player.check_collision()

		# Move the player
		if self.player.moving_down or self.player.moving_up \
			or self.player.moving_right or self.player.moving_left:
			self.player.move(self.window_width * 3, self.dt)
	
		if self.player.interaction:
			self.player.handle_interaction(self.collision)

		# Move the camera
		self.camera.move()

		self.enemy.move()
		self.enemy.adjust_idle_sound(self.player)

	# Game render current state
	def render(self):

		# Draw background, items and props
		self.groups.draw(self.screen, self.camera, self.groups.rendered)

		# Draw the enemy
		self.enemy.draw(self.screen, self.camera)

		# Draw the player
		self.player.draw(self.screen, self.camera)

		# Draw the score
		self.sprites.score.draw(self.screen)

		# Draw interact_box if any
		if self.collision:
			self.sprites.interact_box.draw(self.screen, self.camera)

		# Draw inventory
		self.sprites.inventory.draw(self.screen)

		# Render all images
		pygame.display.flip()

		if self.player.interaction:
			self.player.interaction = None

	# Start level over depending on win or lose
	def end_game(self):
		while self.outro:

			# Draw logo
			#self.sprites.logo.draw_end_scene(self.screen, 300, 100)

			# Render all intro images
			pygame.display.flip()

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.outro = False
	
			# Caps the runtime speed to not kill CPU
			self.clock.tick(60)