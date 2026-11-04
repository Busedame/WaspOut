import pygame
from sprite import Sprite

# Background child class -> inherits from Sprite class
class Background(Sprite):
	def __init__(self, background_name, x, y, scalar):
		super().__init__(f'img/Background/{background_name}.png', x, y, scalar)