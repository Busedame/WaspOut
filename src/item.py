import pygame
from sprite import Sprite

class Item(Sprite):
	def __init__(self, item_name, x, y, scalar, player):
		super().__init__(f'img/Items/{item_name}.png', x, y, scalar)
		self.player = player # Player instance
		self.name = item_name # Name of item

class ItemLadder(Item):
	def __init__(self, item_name, x, y, scalar, player):
		super().__init__(item_name, x, y, scalar, player)

		# Hitbox: middle 50% of ladder width (to make the player more realistically moving in ladder).
		# pygame.Rect(left, top, width, height)
		self.hitbox = pygame.Rect(
			self.rect.centerx - self.rect.width // 2.5, # // means forced integer divison -> so no remainder
			self.rect.top,
			self.rect.width // 2,
			self.rect.height
		)

# Used for items that can be stored in inventory
class ItemInventory(Item):
	def __init__(self, item_name, x, y, scalar, player):
		super().__init__(item_name, x, y, scalar, player)

		# Boolean to check if item is currently picked up by player
		self.picked_up = False

		# Index in inventory (valid from 1).
		self.index = 0

		# Cursor image for this item
		self.cursor = pygame.cursors.Cursor((0, 0), self.image)

	def select_from_inventory(self):
		# Set cursor image
		pygame.mouse.set_cursor(self.cursor)
	
	def deselect_from_inventory(self):
		# Reset cursor image
		pygame.mouse.set_cursor(pygame.cursors.Cursor())

	# Determines which action to perform
	def action(self, action_type, groups):
		if action_type == 'pick up':
			self.pick_up(groups)

		elif action_type == 'drop':
			self.drop(groups)

	# Method to pick up item
	# Ensures that it visually disappears from world, and adds item to inventory
	def pick_up(self, groups):
		self.picked_up = True
		groups.inventory.add(self)
		groups.rendered.remove(self)
		groups.items.remove(self)

		print(f'player picked up {self.name}')

	# Method to drop item
	# Ensures that it visually reappears in world at player's feet, and removes item from inventory
	def drop(self, groups):
		self.picked_up = False
		self.rect.midbottom = (self.player.rect.centerx, self.player.rect.bottom)
		groups.inventory.remove(self)
		groups.rendered.add(self)
		groups.items.add(self)

		print(f'player dropped {self.name} from index {self.index}')
		self.index = 0


# Used for window items.
# There are two different images (opened and close window), and self.image will store
# one of them depending on state of window.
class ItemWindow(Item):
	def __init__(self, item_name, x, y, scalar, player):
		super().__init__(item_name, x, y, scalar, player)

		# Boolean to check if window is currently open
		self.opened = False

		# Closed window image (already initialized in self.image by parent class)
		self.closed_window_image = self.image
		self.closed_window_rect = self.rect
		self.closed_window_rect.center = self.rect.center

		# Opened window image (gets initialized here)
		img = pygame.image.load(f'img/Items/{item_name}_opened.png').convert_alpha()
		self.opened_window_image = pygame.transform.scale(img, (int(img.get_width() * scalar), (int(img.get_height() * scalar))))
		self.opened_window_rect = self.image.get_rect()
		self.opened_window_rect.center = (x, y)
	
	# Determines which action to perform
	def action(self, groups):
		if not self.opened:
			self.open_window()
		else:
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
