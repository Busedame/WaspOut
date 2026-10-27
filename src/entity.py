import pygame
from abc import ABC, abstractmethod

# Parent class to all entities -> can be player, enemy or just a static object.

class Entity(ABC):
	def __init__(self, x: float, y: float, surface: pygame.Surface):
		self.world_pos = pygame.Vector2(x, y)
		self.image = surface
		self.rect = self.image.get_rect(topleft=(x, y))
	
	@abstractmethod
	def draw(self):
		

def init():
	return Entity(2, 3, 'Sprite-test.gif')