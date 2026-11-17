import pygame

class Camera(object):
	def __init__(self, left, top, width, height, player):

		# How far the camera has scrolled (offset)
		self.offset_x = 0

		# Player
		self.player = player

		# Create rect that covers the whole window
		self.rect = pygame.Rect(left, top, width, height)

		# Margin for camera movement (if player is 20 % close to either edge)
		self.player_margin_left = width * 0.20 # Determined by player.rect.x
		self.player_margin_right = width * 0.80 # Determined by player.rect.x + player.rect.w

		# Min/max camera scroll
		self.min_scroll = 0 # Can never go below 0.
		self.max_scroll = self.rect.w * 2 # Can never go above window-size 640 * 2 = 1280 (cause world is 3 * window size), so camera can
		# move in total "two windows".

	def move(self):
		# player.rect.x -> player's world position
		# player_screen_x -> player's screen position
		# self.offset_x -> how far camera has scrolled

		# Player position relative to the screen
		player_screen_x = self.player.rect.x - self.offset_x

		# Left margin
		if player_screen_x < self.player_margin_left:
			self.offset_x -= self.player_margin_left - player_screen_x

		# Right margin
		elif player_screen_x + self.player.rect.w > self.player_margin_right:
			self.offset_x += player_screen_x + self.player.rect.w - self.player_margin_right

		# Prevent camera from scrolling too far left or right
		self.offset_x = max(self.min_scroll, min(self.offset_x, self.max_scroll))
