import pygame
from sprite import Sprite

# Item child class -> inherits from Sprite class
class Item(Sprite):
	def __init__(self, item_name, x, y, scalar, player):
		super().__init__(f'img/Items/{item_name}.png', x, y, scalar)

		self.name = item_name

		self.picked_up = False
		self.player = player

	def action(self, action_type, groups):
		if action_type == 'pick up':
			self.pick_up(groups)

		elif action_type == 'drop':
			self.drop(groups)

	def pick_up(self, groups):
		self.picked_up = True
		groups.inventory.add(self)
		groups.rendered.remove(self)
		groups.items.remove(self)

		print(f'player picked up {self.name}')

	def drop(self, groups):
		self.picked_up = False
		self.rect.midbottom = (self.player.rect.centerx, self.player.rect.bottom)
		groups.inventory.remove(self)
		groups.rendered.add(self)
		groups.items.add(self)

		print(f'player dropped {self.name}')