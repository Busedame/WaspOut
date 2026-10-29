import pygame
from entity import Entity
from background import Background
from props import Props
from camera import Camera

def debug(background: Background, camera: Camera, player: Entity, window: Props):

	# STATIC COMPONENTS
	print ('BACKGROUND')
	print('center: ', background.rect.center)
	print('x: ', background.rect.x, 'y: ', background.rect.y, 'width: ', background.rect.w, 'height: ', background.rect.h)

	print ('WINDOW')
	print('center: ', window.rect.center)
	print('x: ', window.rect.x, 'y: ', window.rect.y, 'width: ', window.rect.w, 'height: ', window.rect.h)

	# DYNAMIC COMPONENTS
	print ('CAMERA')
	print('center: ', camera.rect.center)
	print('x: ', camera.rect.x, 'y: ', camera.rect.y, 'width: ', camera.rect.w, 'height: ', camera.rect.h)

	print ('PLAYER')
	print('center: ', player.rect.center)
	print('x: ', player.rect.x, 'y: ', player.rect.y, 'width: ', player.rect.w, 'height: ', player.rect.h)
