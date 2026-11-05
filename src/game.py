import pygame

def update(groups, sprites, player, enemy, camera):

	# Move the player
	if player.moving_right or player.moving_left:
		player.move()
	
	# Player interacts
	if player.picking_up_item:
		player.pick_up_item()

	if player.capturing_enemy:
		player.capture()

	if player.releasing_enemy:
		player.release()

	if player.dropping_item:
		player.drop_item()

	# Move the camera
	camera.move()

	return player.check_collision(sprites)

def render(groups, sprites, player, enemy, screen, camera, collision):
	# Draw background, items and props
	groups.draw(screen, camera, groups.rendered)

	# Draw the enemy
	enemy.draw(screen, camera)

	# Draw the player
	player.draw(screen, camera)

	# Draw interact_box if any
	if collision:
		sprites.interact_box.draw(screen, camera)

	# Render all images
	pygame.display.flip()