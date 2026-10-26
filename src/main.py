import pygame
import window 
import world
import player

# =======INITIALIZE========

# Initialize pygame modules
pygame.init()

# Initialize screen (create a window surface)
screen = window.init()

# Initialize clock (for FPS calculation)
dt = 0 # Delta time, used to create dynamic FPS based on computer specs.
clock = pygame.time.Clock() # Creates a clock object

# Initialize player
player = player.init()

# Initialize world
world = world.init()

# Main game loop boolean
running = True

# Additional loops
menu = True

# ======MAIN GAME LOOP=====
while running:

	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# Load background
	screen.blit(world.background, (0, 0))

	keys = pygame.key.get_pressed()
	if keys[pygame.K_d] and player.window_pos.x < window.WINDOW_WIDTH - 200:
		player.window_pos.x += 300 * dt
	if keys[pygame.K_a] and player.window_pos.x > 0:
		player.window_pos.x -= 300 * dt

	screen.blit(player.move_right, player.window_pos)
	dt = clock.tick(60) / 1000
	pygame.display.flip()

# Clean up pygame modules
pygame.quit()
