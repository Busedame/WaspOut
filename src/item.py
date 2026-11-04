import pygame

class Item(pygame.sprite.Sprite):
	def __init__(self, item_name, x, y, scalar, player):
		super().__init__()

		img = pygame.image.load(f'img/Items/{item_name}.png')
		self.image = pygame.transform.scale(img, (int(img.get_width() * scalar), (int(img.get_height() * scalar))))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.name = item_name

		self.picked_up = False
		self.player = player
	
	def draw(self, screen, camera):
		# Blits prop on screen relative to camera position
		if self.picked_up == False:
			screen.blit(self.image, (self.rect.x - camera.offset_x, self.rect.y))
	
	def action(self, action_type):
		if action_type == 'pick up':
			self.picked_up = True
			print(f'player picked up {self.name}')
		elif action_type == 'drop':
			self.picked_up = False
			self.rect.midbottom = (self.player.rect.centerx, self.player.rect.centerx)
