import pygame
from entity import Player, Enemy
from background import Background
from props import Prop
from item import ItemInventory, ItemWindow, ItemLadder, Item
from ui import UIInteractionBox, UIInventory

# Every entity (player, enemy) in the world and their initial position is here.
class Entities:
	def __init__(self, window_width, window_height):
		# Characters
		self.player = Player('Player', 200, 300, 3, 150)
		self.enemy = Enemy('Enemy', 175, 200, 3, 10)

# Every sprite (background, item, prop) in the world and their initial position is here.
class Sprites:
	def __init__(self, window_width, window_height, player):

		# Background
		self.bg_upstairs = Background('bg', window_width + (window_width / 2), window_height / 2, 1)
		self.bg_downstairs = Background('bg2', window_width + (window_width / 2), window_height + (window_height / 2), 1)

		# Start text (temp just for fun)
		self.press_space = Prop('press_space', 320, 330, 1)
		self.logo = Prop('logo', 120, 200, 1)

		# Props
		self.fridge = Prop('fridge', 300, 275, 0.70)
		self.oven = Prop('oven', 430, 320, 0.80)
		self.kitchen_counter1 = Prop('kitchen_counter_1', 550, 320, 0.80)
		self.kitchen_counter2 = Prop('kitchen_counter_2', 670, 320, 0.80)
		self.sink = Prop('sink', 650, 235, 0.70)
		self.plates = Prop('plates', 690, 245, 0.70)
		self.flower = Prop('flower', 560, 232, 0.80)
		self.kettle = Prop('kettle', 450, 255, 0.80)
		self.kitchen_counter3 = Prop('kitchen_counter_1', 790, 320, 0.80)
		self.kitchen_picture = Prop('kitchen_picture', 560, 150, 1)
		self.bed = Prop('bed', 1785, 800, 0.90)
		self.sofa = Prop('sofa', 600, 800, 0.90)
		self.bookshelf = Prop('bookshelf', 250, 730, 0.90)
		self.monstera = Prop('monstera', 380, 790, 2)
		self.livingroom_picture = Prop('livingroom_picture', 600, 650, 0.90)
		self.toilet = Prop('toilet', 1070, 300, 1.2)
		self.palm_tree = Prop('palm_tree', 820, 790, 2)
		self.bathroom_sink = Prop('bathroom_sink', 1240, 310, 1)
		self.shower = Prop('shower', 1420, 250, 0.90)
		self.mirror = Prop('mirror', 1240, 210, 1.2)
		self.dresser = Prop('dresser', 1460, 800, 0.90)
		self.bedroom_picture = Prop('bedroom_picture', 1650, 620, 0.90)

		# UI
		self.interact_box = UIInteractionBox('interact_box', 0, 0, 1)
		self.inventory = UIInventory('inventory_slot', window_width - 15, window_height - 15, 1)

		# Inventory items
		self.cup = ItemInventory('cup', 1250, 760, 1, player)
		self.glass = ItemInventory('glass', 1500, 720, 1, player)
		self.paper = ItemInventory('paper', 700, 400, 1, player)
		self.knife = ItemInventory('knife', 790, 260, 1, player)

		# Window items
		self.window = ItemWindow('window', 1200, 680, 0.5, player)

		# Items
		self.ladder = ItemLadder('ladder', 50, 600, 0.80, player)
