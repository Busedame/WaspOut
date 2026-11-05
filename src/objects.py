import pygame
from entity import Player, Enemy
from background import Background
from props import Prop
from item import Item
from ui import UI

# Every entity (player, enemy) in the world and their initial position is here.
class Entities:
	def __init__(self, window_width, window_height):
		# Characters
		self.player = Player('Player', 200, 300, 3, 150)
		self.enemy = Enemy('Enemy', 950, 150, 3, 200)

# Every sprite (background, item, prop) in the world and their initial position is here.
class Sprites:
	def __init__(self, window_width, window_height, player):
		# Background
		self.background = Background('bg', window_width, window_height / 2, 1)

		# Start text (temp just for fun)
		self.press_space = Prop('press_space', 320, 330, 1)
		self.logo = Prop('logo', 420, 200, 1)

		# Props
		self.fridge = Prop('fridge', 200, 260, 0.70)

		# UI
		self.interact_box = UI('interact_box', 0, 0, 1)

		# Items
		self.cup = Item('cup', 950, 280, 1, player)
		self.window = Item('window_tmp', 900, 200, 0.5, player)
