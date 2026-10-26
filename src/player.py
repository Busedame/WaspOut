import pygame
import window
import world

class Player(object):
	window_pos = pygame.Vector2
	world_pos = pygame.Vector2
	idle = pygame.Surface
	move_left = pygame.Surface
	move_right = pygame.Surface
	dead = pygame.Surface

	def __init__(self):
		self.window_pos = pygame.Vector2(0, window.WINDOW_HEIGHT / 2)
		self.world_pos = pygame.Vector2(0, window.WINDOW_HEIGHT / 2)
		self.idle = pygame.image.load('Sprite-test.gif')
		self.move_left = pygame.image.load('Sprite-test.gif')
		self.move_right = pygame.image.load('Sprite-test.gif')
		self.dead = pygame.image.load('Sprite-test.gif')

def init():
	return Player()