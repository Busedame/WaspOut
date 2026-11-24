import pygame

class Sound():

	def __init__(self, sound_type):
		pygame.mixer.init()

		if pygame.mixer.get_init() == None:
			pygame.quit()
			exit(1)
		
		self.sound = pygame.mixer.Sound(f'sounds/{sound_type}')