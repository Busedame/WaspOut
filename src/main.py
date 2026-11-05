import pygame
import game
from objects import Sprites, Entities
from object_groups import ObjectGroups
from camera import Camera
from debug import debug

# Window width and height
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Window init and settings
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Wasp out!')

# Initialize world
entities = Entities(WINDOW_WIDTH, WINDOW_HEIGHT)
sprites = Sprites(WINDOW_WIDTH, WINDOW_HEIGHT, entities.player)

# Initialize groups
groups = ObjectGroups(sprites, entities)

# Reassign player and enemy to separate variables for easier accessibility
player = entities.player
enemy = entities.enemy

# Initialize camera
camera = Camera(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, player)

# Framerate calculation
dt = 0
clock = pygame.time.Clock()

# For running the intro and game loop
running = True
intro = True

# Game intro
while intro:

	# Draw all intro images
	groups.draw(screen, camera, groups.intro)

	# Render all intro images
	pygame.display.flip()

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				intro = False
				running = False
			if event.key == pygame.K_SPACE:
				intro = False
	
	# Caps the runtime speed to not kill CPU
	clock.tick(60)

# Main loop
while running:

	item_collision = game.update(groups, sprites, player, camera)
	game.render(groups, sprites, player, enemy, screen, camera, item_collision)

	# Check for events
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False
		
		# Player actions
		if event.type == pygame.KEYDOWN:
			# Picking up item
			if event.key == pygame.K_w:
				player.picking_up_item = True
			elif event.key == pygame.K_s:
				player.dropping_item = True
			# Moving right
			elif event.key == pygame.K_d:
				player.moving_right = True
			# Moving left
			elif event.key == pygame.K_a:
				player.moving_left = True
			# Exit game
			if event.key == pygame.K_ESCAPE:
				running = False

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_d:
				player.moving_right = False
			if event.key == pygame.K_a:
				player.moving_left = False
			elif event.key == pygame.K_s:
				player.dropping_item = False

	# Get delta time
	dt = clock.tick(60) / 1000

	# DEBUG PRINTS 
	#debug(entities, sprites, camera)

pygame.quit()