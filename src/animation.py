import pygame

# Animation class -> currently hardcoded for entities.
class Animation(object):
	def __init__(self, char_type, motion_type, frames, cooldown):

		self.frames = frames # How many frames for this animation
		self.cooldown = cooldown # How long is the cooldown between frame change
		self.update_time = pygame.time.get_ticks() # Keep track on time to check cooldown
		self.animation_list = [] # Stores each animation frame
		self.frame_index = 0 # Current displayed frame

		# Stores all frames in animation list
		for i in range(frames):
			image = pygame.image.load(f'img/Entity/{char_type}/{motion_type}/{i}.png').convert_alpha()
			self.animation_list.append(image)

		# Initializes image to be first frame of animation list
		self.img = self.animation_list[self.frame_index]

	def update(self):

		# Update image depending on current animation frame
		self.img = self.animation_list[self.frame_index]

		# Check if enough time has passed since last update, and in that case update to next frame.
		if pygame.time.get_ticks() - self.update_time > self.cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		
		# Resets animation if reached end of animation list.
		if self.frame_index >= len(self.animation_list):
			self.frame_index = 0
