import pygame

class Camera(object):
	def __init__(self, left, top, width, height):

		# Create rect that covers the whole window
		self.rect = pygame.Rect(left, top, width, height)

		# Find the middle point of the whole window
		self.rect.center = (width / 2, height / 2)

		# Min/max camera position
		self.min_center_x = width / 2
		self.max_center_x = width * 1.5
	
	def move(self, player):
		pass
		# For player moving right:
		#if player.moving_right:
		#	if 