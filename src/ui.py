import pygame
from sprite import Sprite

class UI(Sprite):
	def __init__(self, background, x, y, scalar):
		super().__init__(f'img/UI/{background}.png', x, y, scalar)

		# Initialize font module
		pygame.font.init()

		# Text
		self.text_font = pygame.font.SysFont("Arial", 10)
		self.text = None

class UIInventory(UI):

	# Reference to inventory to keep track of what is in inventory
	inventory: pygame.sprite.Group

	def __init__(self, background, x, y, scalar):
		super().__init__(background, x, y, scalar)
	
	# For debugging purposes
	def print_items(self):
		print("ITEMS IN INVENTORY:")
		for item in self.inventory:
			print(item.name)

	# Draws inventory boxes depending on how many items are present
	def draw(self, screen):
		item_pos_x_offset = 0

		for item in self.inventory:
			screen.blit(self.image, (self.rect.x - item_pos_x_offset, self.rect.y))
			screen.blit(item.image, (self.rect.x - item_pos_x_offset, self.rect.y))
			item_pos_x_offset += self.rect.w

class UIScore(UI):

	def __init__(self, background, x, y, scalar, player):

		super().__init__(background, x, y, scalar)
		# Initialize font module
		pygame.font.init()

		# Text
		self.text_font = pygame.font.SysFont("Arial", 20, True)
		self.text = None
		self.color = (238, 170, 0)

		self.player = player
	
	def draw(self, screen):
		screen.blit(self.image, (self.rect.x, self.rect.y))
		self.text = self.text_font.render(f'Wasps removed: {self.player.score}', True, self.color)
		screen.blit(self.text, (0, 0))
	

class UIInteractionBox(UI):
	def __init__(self, background, x, y, scalar):
		super().__init__(background, x, y, scalar)

	# Interaction box action
	def action(self, player, action_type, target):
		self.rect.x = player.rect.x + player.rect.w # Set the background rect
		self.rect.y = player.rect.y # Set the background rect

		if action_type == 'pick up':
			self.pick_up(player, target)
		elif action_type == 'capture':
			self.capture(player, target)
		elif action_type == 'window':
			self.window(player, target)

	# Interaction box -> handle pick up item
	def pick_up(self, player, item):
		if not item.picked_up:
			self.text = self.text_font.render(f'pick up {item.name}: e', True, (255, 255, 255))
		else:
			self.text = None

	# Interaction box -> handle capture enemy
	def capture(self, player, enemy):
		self.text = self.text_font.render(f'capture wasp: e', True, (255, 255, 255))

	# Interaction box -> handle open or close window, or release enemy through window
	def window(self, player, target):
		if not target.opened:
			self.text = self.text_font.render(f'open {target.name}: e', True, (255, 255, 255))
		elif target.opened and player.enemy_captured:
			self.text = self.text_font.render(f'release wasp: r', True, (255, 255, 255))
		else:
			self.text = self.text_font.render(f'close {target.name}: r', True, (255, 255, 255))

	# Super class (Sprite) instance draws the textbox
	# UI class (self) instance draws the text
	def draw(self, screen, camera):
		if self.text is not None:
			super().draw(screen, camera)
			text_rect = self.text.get_rect(center=self.rect.center)
			screen.blit(self.text, (text_rect.x - camera.offset_x, text_rect.y - camera.offset_y))
			self.text = None