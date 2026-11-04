import pygame
from entity import Entity, Player, Enemy
from background import Background
from props import Prop
from item import Item

# Every object in the world and their initial position is here.
class Sprites:
	def __init__(self, window_width, window_height):
		# Background
		self.background = Background(window_width, window_height / 2)

		# Start text (temp just for fun)
		self.press_space = Prop('press_space', 320, 330, 1)
		self.logo = Prop('logo', 420, 200, 1)

		# Props
		self.fridge = Prop('fridge', 200, 260, 0.80)

		# Characters
		self.player = Player('Player', 200, 300, 3, 150)
		self.enemy = Enemy('Enemy', 950, 150, 3, 200)

		# Items
		self.cup = Item('cup', 950, 280, 1, self.player)
		self.window = Item('window_tmp', 900, 200, 0.5, self.player)

# Every sprite group in the world and their initial members are here.
class SpriteGroups:
	def __init__(self, sprites):
		# Intro
		self.intro = pygame.sprite.Group(sprites.background, sprites.fridge, sprites.press_space, sprites.logo)

		# Characters
		self.player = pygame.sprite.GroupSingle(sprites.player)
		self.enemies = pygame.sprite.Group(sprites.enemy)

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
			sprites.enemy,
			sprites.player
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