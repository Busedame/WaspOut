import pygame
import window 
import world
import player
import camera

# =======INITIALIZE========

# Initialize pygame modules
pygame.init()

# Initialize screen (create a window surface)
screen = window.init()

# Initialize clock (for FPS calculation)
dt = 0 # Delta time, used to create dynamic FPS based on computer specs.
clock = pygame.time.Clock() # Creates a clock object

# Intiialize camera
game_camera = camera.init()

# Initialize player
game_player = player.init(game_camera)

# Initialize world
game_world = world.init()

# Main game loop boolean
running = True

# Additional loops
menu = True

# ======MAIN GAME LOOP=====
while running:

	print("Player world coordinates: ", game_player.world_pos.x, game_player.world_pos.y)
	print("Player window coordinates: ", game_player.window_pos.x, game_player.window_pos.y)
	print("Camera world coordinates: ", game_camera.pos.x)
	# Get delta time.
	dt = clock.tick(60) / 1000

	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	player_width = game_player.idle.get_width()
	print("Player width: ", player_width)

	keys = pygame.key.get_pressed()
	if keys[pygame.K_d]:
		game_player.world_pos.x += 300 * dt
	if keys[pygame.K_a]:
		game_player.world_pos.x -= 300 * dt


	# Keep player inside world boundaries
	game_player.world_pos.x = max(0, min(game_player.world_pos.x, world.WORLD_WIDTH - player_width))

	# Update camera view
	game_camera.update(game_player.world_pos.x)

	# Load background
	screen.blit(game_world.background, (-game_camera.left_edge, 0))

	# Update player's position in the window
	game_player.window_pos.x = game_player.world_pos.x - game_camera.left_edge

	# Draw the player's new position.
	screen.blit(game_player.move_right, (game_player.window_pos.x, game_player.window_pos.y))

	# Update the screen
	pygame.display.flip()

# Clean up pygame modules
pygame.quit()
