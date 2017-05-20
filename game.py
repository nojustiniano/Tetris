import copy
import random
import pygame
import sys
from pygame.locals import *

from collision import Collision
from figure import figure_list
from properties import Properties
from stage import Stage


class Game:

    def start_game(self):
        pygame.init()
        pygame.display.set_caption("Tetris")
        screen = pygame.display.set_mode(
            (Properties.BLOCK_SIZE * Properties.STAGE_WIDTH, Properties.BLOCK_SIZE * Properties.STAGE_HEIGHT))

        clock = pygame.time.Clock()
        stage = Stage()
        collision = Collision(stage)
        rotated = 0
        gravity = 0
        figure = self.get_random_figure()
        next_figure = self.get_random_figure()

        while True:
            screen.fill((0, 0, 0))
            stage.draw(screen)
            figure.draw(screen)
            pygame.display.update()
            move_x = 0
            move_y = 0

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(True)

            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_DOWN]:
                move_y = 1
            if pressed[pygame.K_LEFT]:
                move_x = -1
            if pressed[pygame.K_RIGHT]:
                move_x = 1
            if pressed[pygame.K_a]:
                if rotated == 0:
                    figure.rotate_left()
                    rotated = 1
            if pressed[pygame.K_d]:
                if rotated == 0:
                    figure.rotate_right()
                    rotated = 1

            if 0 < rotated < 3:
                rotated += 1
            else:
                rotated = 0

            if gravity < 8:
                gravity += 1
            else:
                gravity = 0
                move_y = 1

            if collision.check_x(figure, move_x):
                move_x = 0
                print("collide")

            figure.x += move_x

            if collision.check_y(figure, move_y):
                move_y = 0
                stage.merge_figure(figure)
                figure = next_figure
                next_figure = self.get_random_figure()
                print("merge")

            figure.y += move_y

            stage.check_completed_lines()

            clock.tick(10)

    @staticmethod
    def get_random_figure():
        figure = copy.copy(figure_list[random.randint(0, len(figure_list) - 1)])
        figure.x = random.randint(0, Properties.STAGE_WIDTH - 1 - figure.width)
        figure.y = 0
        return figure
