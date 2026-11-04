import pygame

# Every group in the world and their initial members are here.
class ObjectGroups:
	def __init__(self, sprites, entities):
		# Intro
		self.intro = pygame.sprite.Group(sprites.background, sprites.fridge, sprites.press_space, sprites.logo)

		# Characters
		self.player = pygame.sprite.GroupSingle(entities.player)
		self.enemies = pygame.sprite.Group(entities.enemy)

		# All items in game
		self.items = pygame.sprite.Group(sprites.cup, sprites.window)

		# Items currently carried
		self.inventory = pygame.sprite.Group()

		# Props
		self.props = pygame.sprite.Group(sprites.fridge)

		# Objects belonging to each floor
		self.upstairs = pygame.sprite.Group(
			sprites.background,
			sprites.fridge,
			sprites.window,
			sprites.cup,
			entities.enemy,
			entities.player
		)
		self.downstairs = pygame.sprite.Group()

		# All objects currently rendered (can be background, items, props)
		self.rendered = pygame.sprite.Group(
			sprites.background,
			sprites.fridge,
			sprites.window,
			sprites.cup
		)

	# A custom draw method to make sure camera movement works.
	# Calls each sprite's individual draw method.
	def draw(self, screen, camera, group):
		for sprite in group:
			sprite.draw(screen, camera)
