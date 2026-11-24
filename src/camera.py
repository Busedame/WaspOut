import pygame

class Camera(object):
	def __init__(self, left, top, width, height, player):

		# How far the camera has scrolled (offset)
		self.offset_x = 0
		self.offset_y = 0

		# Player
		self.player = player

		# Create rect that covers the whole window
		self.rect = pygame.Rect(left, top, width, height)

		# Margin for x-axis camera movement (if player is 20 % close to either edge)
		self.player_margin_left = width * 0.20 # Determined by player.rect.x
		self.player_margin_right = width * 0.80 # Determined by player.rect.x + player.rect.w

		# Margin for y-axis camera movement (if player is 10 % close to either edge)
		self.player_margin_top = height * 0.10
		self.player_margin_bottom = height * 0.90

		# Min/max camera scroll (for x-axis)
		self.min_scroll = 0 # Can never go below 0.
		self.max_scroll = self.rect.w * 2 # Can never go above window-size 640 * 2 = 1280 (cause world is 3 * window size), so camera can
		# move in total "two windows".

	def move(self):
		# player.rect.x -> player's world position
		# player_screen_x -> player's screen position
		# self.offset_x -> how far camera has scrolled

		#### X-AXIS ####

		# Player position relative to the screen
		player_screen_x = self.player.rect.x - self.offset_x

		# Left margin
		if player_screen_x < self.player_margin_left:
			self.offset_x -= self.player_margin_left - player_screen_x

		# Right margin
		elif player_screen_x + self.player.rect.w > self.player_margin_right:
			self.offset_x += player_screen_x + self.player.rect.w - self.player_margin_right
		
		# Prevent camera from scrolling too far left or right
		if self.player.rect.y == self.player.min_y:
			self.offset_x = max(self.min_scroll, min(self.offset_x, self.max_scroll - 400)) # Hardcoded to cut off background on right side
		else:
			self.offset_x = max(self.min_scroll, min(self.offset_x, self.max_scroll))

		#### Y-AXIS ####

		# Determine target camera position based on player position
		if self.player.rect.y < 400:
			target_y = 0
		else:
			target_y = self.rect.h

		# Automove camera towards target
		speed = 5

		if self.offset_y < target_y:
			self.offset_y = min(self.offset_y + speed, target_y)

		elif self.offset_y > target_y:
			self.offset_y = max(self.offset_y - speed, target_y)
