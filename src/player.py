import pygame
import window
import world
import camera

class Player(object):
	def __init__(self, game_camera):
		self.window_pos = pygame.Vector2(window.WINDOW_WIDTH / 2, window.WINDOW_HEIGHT / 2)
		self.world_pos = pygame.Vector2(window.WINDOW_WIDTH / 2, window.WINDOW_HEIGHT / 2)

		# Image states
		self.idle = pygame.image.load('Sprite-test.gif')
		self.move_left = pygame.image.load('Sprite-test.gif')
		self.move_right = pygame.image.load('Sprite-test.gif')
		self.dead = pygame.image.load('Sprite-test.gif')

		self.rect = self.idle.get_rect(topleft=(self.window_pos.x, self.window_pos.y))

def init(game_camera):
	return Player(game_camera)