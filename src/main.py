import pygame
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

	# Draw background, items and props
	groups.draw(screen, camera, groups.rendered)

	# Draw the player
	player.draw(screen, camera)

	# Draw the enemy
	enemy.draw(screen, camera)

	# Render all images
	pygame.display.flip()

	# Check for events
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				player.is_interacting = True
			elif event.key == pygame.K_d and player.is_interacting == False:
				player.moving_right = True
			elif event.key == pygame.K_a and player.is_interacting == False:
				player.moving_left = True
			if event.key == pygame.K_ESCAPE:
				running = False

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_d:
				player.moving_right = False
			if event.key == pygame.K_a:
				player.moving_left = False

	# Get delta time
	dt = clock.tick(60) / 1000

	# Move the player
	player.move()

	# Move the camera
	camera.move()

	# DEBUG PRINTS 
	debug(entities, sprites, camera)

pygame.quit()