import pygame
from objects import Entities, Sprites
from camera import Camera

def debug(entities: Entities, sprites: Sprites, camera: Camera):

	# STATIC COMPONENTS
	print('BACKGROUND')
	print('center: ', sprites.background.rect.center)
	print('x: ', sprites.background.rect.x, 'y: ', sprites.background.rect.y, 'width: ', sprites.background.rect.w, 'height: ', sprites.background.rect.h)

	# DYNAMIC COMPONENTS
	print('CAMERA')
	print('center: ', camera.rect.center)
	print('x: ', camera.rect.x, 'y: ', camera.rect.y, 'width: ', camera.rect.w, 'height: ', camera.rect.h)
	print('margin left: ', camera.player_margin_left, 'margin right:', camera.player_margin_right)

	print('PLAYER')
	print('center: ', entities.player.rect.center)
	print('x: ', entities.player.rect.x, 'y: ', entities.player.rect.y, 'width: ', entities.player.rect.w, 'height: ', entities.player.rect.h)

	print('ENEMY')
	print('center: ', entities.enemy.rect.center)
	print('x: ', entities.enemy.rect.x, 'y: ', entities.enemy.rect.y, 'width: ', entities.enemy.rect.w, 'height: ', entities.enemy.rect.h)

	print('CAMERA MOVEMENT')
	print('Camera offset x: ', camera.offset_x)
	print('Camera left margin: ', camera.player_margin_left)
	print('Camera right margin: ', camera.player_margin_right)
	print('Player screen x: ', entities.player.rect.x - camera.offset_x)
	print('Background x: ', sprites.background.rect.x - camera.offset_x)
	print('Window x: ', sprites.window.rect.x - camera.offset_x)
	print('Enemy x: ', entities.enemy.rect.x - camera.offset_x)

	print('WINDOW')
	print('center: ', sprites.window.rect.center)
	print('x: ', sprites.window.rect.x, 'y: ', sprites.window.rect.y, 'width: ', sprites.window.rect.w, 'height: ', sprites.window.rect.h)

	print('CUP')
	print('center: ', sprites.cup.rect.center)

	print('PAPER')
	print('center: ', sprites.paper.rect.center)