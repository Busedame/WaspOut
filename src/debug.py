import pygame
from entity import Entity
from background import Background
from props import Prop
from camera import Camera
from item import Item

def debug(background: Background, camera: Camera, player: Entity, enemy: Entity, window1: Prop, window2: Prop, cup: Item):

	# STATIC COMPONENTS
	print ('BACKGROUND')
	print('center: ', background.rect.center)
	print('x: ', background.rect.x, 'y: ', background.rect.y, 'width: ', background.rect.w, 'height: ', background.rect.h)

	print ('WINDOW1')
	print('center: ', window1.rect.center)
	print('x: ', window1.rect.x, 'y: ', window1.rect.y, 'width: ', window1.rect.w, 'height: ', window1.rect.h)

	print ('WINDOW2')
	print('center: ', window2.rect.center)
	print('x: ', window2.rect.x, 'y: ', window2.rect.y, 'width: ', window2.rect.w, 'height: ', window2.rect.h)

	# DYNAMIC COMPONENTS
	print ('CAMERA')
	print('center: ', camera.rect.center)
	print('x: ', camera.rect.x, 'y: ', camera.rect.y, 'width: ', camera.rect.w, 'height: ', camera.rect.h)
	print('margin left: ', camera.player_margin_left, 'margin right:', camera.player_margin_right)

	print ('PLAYER')
	print('center: ', player.rect.center)
	print('x: ', player.rect.x, 'y: ', player.rect.y, 'width: ', player.rect.w, 'height: ', player.rect.h)

	print ('ENEMY')
	print('center: ', enemy.rect.center)
	print('x: ', enemy.rect.x, 'y: ', enemy.rect.y, 'width: ', enemy.rect.w, 'height: ', enemy.rect.h)

	print('CAMERA MOVEMENT')
	print('Camera offset x: ', camera.offset_x)
	print('Camera left margin: ', camera.player_margin_left)
	print('Camera right margin: ', camera.player_margin_right)
	print('Player screen x: ', player.rect.x - camera.offset_x)
	print('Background x: ', background.rect.x - camera.offset_x)
	print('Window1 x: ', window1.rect.x - camera.offset_x)
	print('Window2 x: ', window2.rect.x - camera.offset_x)
	print('Enemy x: ', enemy.rect.x - camera.offset_x)

	print('CUP')
	print('center: ', cup.rect.center)