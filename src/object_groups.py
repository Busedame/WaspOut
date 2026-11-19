import pygame

# Every group in the world and their initial members are here.
class ObjectGroups:
	def __init__(self, sprites, entities):
		# Intro
		self.intro = pygame.sprite.Group(
			sprites.bg_upstairs,
			sprites.bg_downstairs,
			sprites.ladder,
			sprites.kitchen_picture,
			sprites.fridge,
			sprites.kettle,
			sprites.flower,
			sprites.oven,
			sprites.plates,
			sprites.kitchen_counter1,
			sprites.kitchen_counter2,
			sprites.kitchen_counter3,
			sprites.sink,
			sprites.window,
			sprites.cup,
			sprites.paper,
			sprites.knife,
			sprites.logo,
			sprites.press_space
		)

		# Outro
		self.outro = pygame.sprite.Group(sprites.bg_upstairs, sprites.fridge, sprites.logo)

		# Characters
		self.player = pygame.sprite.GroupSingle(entities.player)
		self.enemies = pygame.sprite.Group(entities.enemy)

		# All items in game
		self.items = pygame.sprite.Group(sprites.cup, sprites.window, sprites.paper, sprites.ladder, sprites.knife)

		# Items currently carried
		self.inventory = pygame.sprite.Group()

		# Props
		self.props = pygame.sprite.Group(sprites.fridge, sprites.kitchen_picture, sprites.oven, sprites.kitchen_counter1, sprites.kitchen_counter2, sprites.kitchen_counter3, sprites.sink, sprites.plates, sprites.kettle, sprites.flower, sprites.bed)

		# UI
		self.UI = pygame.sprite.Group(sprites.interact_box, sprites.inventory)

		# Objects belonging to each floor
		self.upstairs = pygame.sprite.Group(
			sprites.bg_upstairs,
			sprites.fridge,
			sprites.oven,
			sprites.window,
			sprites.cup,
			sprites.paper,
			entities.enemy,
			entities.player
		)
		self.downstairs = pygame.sprite.Group(
			sprites.bg_downstairs,
			sprites.ladder
		)

		# All objects currently rendered (can be bg_upstairs, items, props)
		self.rendered = pygame.sprite.Group(
			sprites.bg_upstairs,
			sprites.bg_downstairs,
			sprites.ladder,
			sprites.kitchen_picture,
			sprites.fridge,
			sprites.kettle,
			sprites.oven,
			sprites.plates,
			sprites.kitchen_counter1,
			sprites.kitchen_counter2,
			sprites.kitchen_counter3,
			sprites.sink,
			sprites.flower,
			sprites.window,
			sprites.cup,
			sprites.paper,
			sprites.knife,
			sprites.bed
		)

		# Assign properties to player
		entities.player.inventory = self.inventory
		entities.player.groups = self
		entities.player.sprites = sprites

		# Assign inventory group to inventory 
		sprites.inventory.inventory = self.inventory


	# A custom draw method to make sure camera movement works.
	# Calls each sprite's individual draw method.
	def draw(self, screen, camera, group):
		for sprite in group:
			sprite.draw(screen, camera)
