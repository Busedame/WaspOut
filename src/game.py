import pygame

def update(groups, sprites, player, camera):

	# Move the player
	player.move()

	# Move the camera
	camera.move()

	# Check for item collision
	item = player.check_item_collision(groups.items)
	if item:
		sprites.interact_box.set_interact_box(player, item)
		return True
	
	return False

def render(groups, sprites, player, enemy, screen, camera, item_collision):
	# Draw background, items and props
	groups.draw(screen, camera, groups.rendered)

	# Draw the player
	player.draw(screen, camera)

	# Draw the enemy
	enemy.draw(screen, camera)

	# Draw interact_box if any
	if item_collision:
		sprites.interact_box.draw(screen, camera)

	# Render all images
	pygame.display.flip()