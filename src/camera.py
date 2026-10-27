# Controls the camera view
import pygame
import window
import player
import world

class Camera(object):
	def __init__(self):
		self.pos = pygame.Vector2(window.WINDOW_WIDTH / 2, window.WINDOW_HEIGHT / 2) # The starting position of camera
		self.margin = window.WINDOW_WIDTH * 0.20 # 20 % close to either side (left or right) will trigger camera movement, if there is more to reveal.

	@property
	# Helper function -> defines where the left edge of camera view currently is.
	def left_edge(self):
		return self.pos.x - (window.WINDOW_WIDTH / 2)

	# Update the camera position
	def update(self, player_world_pos_x: int):

		# Find where the player is relative to what is displayed on SCREEN right now.
		player_screen_x = player_world_pos_x - self.left_edge

		# Calculate if camera should move:

		# If player is pushing to the LEFT margin.
		if player_screen_x < self.margin:
	
			# Camera moves so player STAYS on LEFT margin.
			self.pos.x = player_world_pos_x + (window.WINDOW_WIDTH / 2) - self.margin

		# If player is pushing to the RIGHT margin.
		elif player_screen_x > window.WINDOW_WIDTH - self.margin:

			# Camera moves so player STAYS on RIGHT margin.
			self.pos.x = player_world_pos_x - (window.WINDOW_WIDTH / 2) + self.margin

		# Calculate if camera is already at the end
		min_camera_x = window.WINDOW_WIDTH / 2
		max_camera_x = world.WORLD_WIDTH - (window.WINDOW_WIDTH / 2)

		# If camera is already at either end, set camera to min or max value.
		if self.pos.x < min_camera_x:
			self.pos.x = min_camera_x
		elif self.pos.x > max_camera_x:
			self.pos.x = max_camera_x

def init():
	return Camera()