import pygame
from sprite import Sprite

# Item child class -> inherits from Sprite class
class Item(Sprite):
	def __init__(self, item_name, x, y, scalar, player):
		super().__init__(f'img/Items/{item_name}.png', x, y, scalar)

		self.name = item_name

		self.picked_up = False
		self.player = player
	
	def draw(self, screen, camera):
		# Blits prop on screen relative to camera position
		if not self.picked_up:
			super().draw(screen, camera)
	
	def action(self, action_type):
		if action_type == 'pick up':
			self.picked_up = True
			print(f'player picked up {self.name}')
		elif action_type == 'drop':
			self.picked_up = False
			self.rect.midbottom = (self.player.rect.centerx, self.player.rect.bottom)
