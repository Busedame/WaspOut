import pygame
from entity import Entity
from background import Background
from props import Props
from camera import Camera
from debug import debug

# Window width and height
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Window init and settings
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Wasp out!')

# Start text (temp just for fun)
press_space = Props('press_space', 320, 330, 1)
logo = Props('logo', 420, 200, 1)

# Initialize player instance
player = Entity('Player', 200, 300, 3, 150)

# Initialize enemy instance
enemy = Entity('Enemy', 950, 150, 3, 200)

# Initialize background instance
background = Background(WINDOW_WIDTH, WINDOW_HEIGHT / 2)

# Initialize props (Temp, should be initialized as an array)
window1 = Props('window_tmp', 200, 200, 0.5)
window2 = Props('window_tmp', 900, 200, 0.5)
cup = Props('cup', 250, 280, 1)

# Initialize camera
camera = Camera(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, player)

# Framerate calculation
dt = 0
clock = pygame.time.Clock()

# For running the intro and game loop
running = True
intro = True

while intro:
	background.draw(screen, camera)
	window1.draw(screen, camera)
	logo.draw(screen, camera)
	press_space.draw(screen, camera)

	# Render all images
	pygame.display.flip()

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				intro = False
				running = False
			if event.key == pygame.K_SPACE:
				intro = False

while running:

	# Draw the background and props
	background.draw(screen, camera)
	window1.draw(screen, camera)
	window2.draw(screen, camera)
	cup.draw(screen, camera)

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
			if event.key == pygame.K_d:
				player.moving_right = True
			if event.key == pygame.K_a:
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
	debug(background, camera, player, enemy, window1, window2)

pygame.quit()