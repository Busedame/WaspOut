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

# Initialize player instance
player = Entity('Player', 200, 300, 3)

# Initialize background instance
background = Background(WINDOW_WIDTH, WINDOW_HEIGHT / 2)

# Initialize props (Temp, should be initialized as an array)
window = Props('window_tmp', 200, 200, 0.5)

# Initialize camera
camera = Camera(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

# Framerate calculation
dt = 0
clock = pygame.time.Clock()

# Running the game loop
running = True

while running:

	# Draw the background and props
	background.draw(screen)
	window.draw(screen)

	# Draw the player
	player.draw(screen)

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

	# DEBUG PRINTS 
	debug(background, camera, player, window)

pygame.quit()