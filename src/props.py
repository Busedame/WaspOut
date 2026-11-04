import pygame
from sprite import Sprite

class Prop(Sprite):
	def __init__(self, prop_name, x, y, scalar):
		super().__init__(f'img/Props/{prop_name}.png', x, y, scalar)