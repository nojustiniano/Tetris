import pygame, sys
from pygame.locals import *

from tetris.collision import Collision
from tetris.figure import t_figure
from tetris.stage import Stage

pygame.init()
pygame.display.set_caption("Tetris")
screen = pygame.display.set_mode((480, 864))

clock = pygame.time.Clock()
stage = Stage()
collision = Collision(stage)

t_figure.position.set(4, 0)
while True:
    screen.fill((0, 0, 0))
    stage.draw(screen)
    t_figure.draw(screen)
    pygame.display.update()
    move_x = 0
    move_y = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(True)
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_DOWN:
        #         move_y = 1
        #     if event.key == pygame.K_LEFT:
        #         move_x = -1
        #     if event.key == pygame.K_RIGHT:
        #         print("right")
        #         move_x = 1

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_DOWN]:
        move_y = 1
    elif pressed[pygame.K_LEFT]:
        move_x = -1
    elif pressed[pygame.K_RIGHT]:
        move_x = 1
    elif pressed[pygame.K_a]:
        t_figure.rotate_left()
    elif pressed[pygame.K_d]:
        t_figure.rotate_right()

    if collision.check_borders(t_figure, move_x):
        move_x = 0
        print("collide")
    if collision.check_stage(t_figure, move_x, move_y):
        move_x = 0
        move_y = 0
        stage.merge_figure(t_figure)
        t_figure.position.set(2, 0)
        print("merge")

    t_figure.position.x += move_x
    t_figure.position.y += move_y
    clock.tick(10)
