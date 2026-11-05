import pygame
from sprite import Sprite

class Prop(Sprite):
	def __init__(self, prop_name, x, y, scalar):
		super().__init__(f'img/Props/{prop_name}.png', x, y, scalar)
	
	def set_interact_box(self, player):
		self.rect.x = player.rect.x + player.rect.w
		self.rect.y = player.rect.y