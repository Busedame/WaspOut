import pygame
from sprite import Sprite

class Item(Sprite):
	def __init__(self, item_name, x, y, scalar, player):
		super().__init__(f'img/Items/{item_name}.png', x, y, scalar)
		self.player = player
		self.name = item_name

# Used for items that can be stored in inventory
class ItemInventory(Item):
	def __init__(self, item_name, x, y, scalar, player):
		super().__init__(item_name, x, y, scalar, player)

		self.picked_up = False

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


# Used for window items
class ItemWindow(Item):
	def __init__(self, item_name, x, y, scalar, player):
		super().__init__(item_name, x, y, scalar, player)

		self.opened = False

		self.closed_window_image = self.image
		self.closed_window_rect = self.rect
		self.closed_window_rect.center = self.rect.center

		img = pygame.image.load(f'img/Items/{item_name}_opened.png').convert_alpha()
		self.opened_window_image = pygame.transform.scale(img, (int(img.get_width() * scalar), (int(img.get_height() * scalar))))
		self.opened_window_rect = self.image.get_rect()
		self.opened_window_rect.center = (x, y)
	
	def action(self, action_type, groups):
		if action_type == 'open' and not self.opened:
			self.open_window()
		elif action_type == 'close' and self.opened:
			self.close_window()

	# Method to open window
	# Changes image and window state
	def open_window(self):
		self.image = self.opened_window_image
		self.opened = True

		print(f'player opened {self.name}')

	# Method to close window
	# Changes image and window state
	def close_window(self):
		self.image = self.closed_window_image
		self.opened = False
	
		print(f'player closed {self.name}')
