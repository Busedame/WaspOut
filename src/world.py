import pygame
import window

# World dimensions
WORLD_WIDTH = window.WINDOW_WIDTH * 2
WORLD_HEIGHT = window.WINDOW_HEIGHT

class World(object):
	def __init__(self):
		self.background = pygame.image.load('background.png').convert()
		self.width = WORLD_WIDTH
		self.height = WORLD_HEIGHT

def init():
	return World()
