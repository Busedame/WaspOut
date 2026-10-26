import pygame

# Window dimensions
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Initialize window with window dimensions
def init():
	pygame.display.set_caption("Wasp out!")
	#return pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
	return pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

