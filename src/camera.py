import pygame

class Camera(object):
	def __init__(self, left, top, width, height):
		self.rect = pygame.Rect(left, top, width, height)
		self.rect.center = (width / 2, height / 2)
		