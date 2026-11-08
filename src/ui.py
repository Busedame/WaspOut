import pygame
from sprite import Sprite

class UI(Sprite):
	def __init__(self, prop_name, x, y, scalar):
		super().__init__(f'img/UI/{prop_name}.png', x, y, scalar)

		pygame.font.init()

		# Text
		self.text_font = pygame.font.SysFont("Arial", 10)
		self.text_image = None

	def action(self, player, action_type, target):
		self.rect.x = player.rect.x + player.rect.w
		self.rect.y = player.rect.y

		if action_type == 'pick up':
			self.pick_up(player, target)
		elif action_type == 'capture':
			self.capture(player, target)
		elif action_type == 'window':
			self.window(player, target)

	def pick_up(self, player, item):
		if not item.picked_up:
			self.text_image = self.text_font.render(f'pick up {item.name}: w', True, (255, 255, 255))
		else:
			self.text_image = None

	def capture(self, player, enemy):
		self.text_image = self.text_font.render(f'capture wasp: w', True, (255, 255, 255))

	def window(self, player, target):
		if not target.opened:
			self.text_image = self.text_font.render(f'open {target.name}: w', True, (255, 255, 255))
		elif target.opened and player.enemy_captured:
			self.text_image = self.text_font.render(f'release wasp: s', True, (255, 255, 255))
		else:
			self.text_image = self.text_font.render(f'close {target.name}: s', True, (255, 255, 255))

	def draw(self, screen, camera):
		if self.text_image is not None:
			super().draw(screen, camera)
			text_rect = self.text_image.get_rect(center=self.rect.center)
			screen.blit(self.text_image, (text_rect.x - camera.offset_x, text_rect.y))
