import pygame
from entity import Entity
from background import Background

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Window init and settings
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Wasp out!')

# Initialize player instance
player = Entity('Player', 200, 350, 3)
moving_right = False
moving_left = False

# Initialize background instance
background = Background(WINDOW_WIDTH, WINDOW_HEIGHT / 2)

# Framerate calculation
dt = 0
clock = pygame.time.Clock()

# Running the game loop
running = True

while running:

	dt = clock.tick(60) / 1000
	background.draw(screen)
	player.move(moving_right, moving_left)
	player.draw(screen)

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_d:
				moving_right = True
			if event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_ESCAPE:
				running = False
		
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_d:
				moving_right = False
			if event.key == pygame.K_a:
				moving_left = False
	

	pygame.display.flip()

pygame.quit()