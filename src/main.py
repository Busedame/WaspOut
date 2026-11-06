import pygame
from debug import debug
from game import Game

# Creates game object
game = Game()

# Starts game intro
game.intro_loop()

# Starts game
game.main_loop()

# Quits pygame module
pygame.quit()