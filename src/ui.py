import pygame
from sprite import Sprite

class UI(Sprite):
	def __init__(self, prop_name, x, y, scalar):
		super().__init__(f'img/UI/{prop_name}.png', x, y, scalar)

		pygame.font.init()

		# Text
		self.text_font = pygame.font.SysFont("Arial", 10)
		self.text_image = None
	
	def set_interact_box(self, player, item):
		self.rect.x = player.rect.x + player.rect.w
		self.rect.y = player.rect.y

		# Actions
		if not item.picked_up:
			self.text_image = self.text_font.render(f'pick up {item.name}: w', True, (255, 255, 255))
		else:
			self.text_image = None

	def draw(self, screen, camera):
		if self.text_image is not None:
			super().draw(screen, camera)
			text_rect = self.text_image.get_rect(center=self.rect.center)
			screen.blit(self.text_image, (text_rect.x - camera.offset_x, text_rect.y))
