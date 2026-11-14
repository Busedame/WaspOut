import pygame

# Every group in the world and their initial members are here.
class ObjectGroups:
	def __init__(self, sprites, entities):
		# Intro
		self.intro = pygame.sprite.Group(sprites.background, sprites.fridge, sprites.press_space, sprites.logo)

		# Outro
		self.outro = pygame.sprite.Group(sprites.background, sprites.fridge, sprites.logo)

		# Characters
		self.player = pygame.sprite.GroupSingle(entities.player)
		self.enemies = pygame.sprite.Group(entities.enemy)

		# All items in game
		self.items = pygame.sprite.Group(sprites.cup, sprites.window, sprites.paper)

		# Items currently carried
		self.inventory = pygame.sprite.Group()

		# Props
		self.props = pygame.sprite.Group(sprites.fridge)

		# UI
		self.UI = pygame.sprite.Group(sprites.interact_box)

		# Objects belonging to each floor
		self.upstairs = pygame.sprite.Group(
			sprites.background,
			sprites.fridge,
			sprites.window,
			sprites.cup,
			sprites.paper,
			entities.enemy,
			entities.player
		)
		self.downstairs = pygame.sprite.Group()

		# All objects currently rendered (can be background, items, props)
		self.rendered = pygame.sprite.Group(
			sprites.background,
			sprites.fridge,
			sprites.window,
			sprites.cup,
			sprites.paper
		)

		# Assign inventory to player
		entities.player.inventory = self.inventory
		entities.player.groups = self
		entities.player.sprites = sprites

	# A custom draw method to make sure camera movement works.
	# Calls each sprite's individual draw method.
	def draw(self, screen, camera, group):
		for sprite in group:
			sprite.draw(screen, camera)
