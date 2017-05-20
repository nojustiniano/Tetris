import copy
import random
import pygame
import sys
from pygame.locals import *

from collision import Collision
from figure import figure_list
from menu import Menu
from properties import Properties
from stage import Stage


class Game:
    def start_game(self):
        pygame.init()
        pygame.display.set_caption("Tetris")

        screen = pygame.display.set_mode(
            (Properties.BLOCK_SIZE * Properties.STAGE_WIDTH + Properties.MENU_WIDTH + 3 * Properties.WINDOW_BORDER_WIDTH,
             Properties.BLOCK_SIZE * Properties.STAGE_HEIGHT + 2 * Properties.WINDOW_BORDER_WIDTH))
        stage_surface = pygame.Surface(
            (Properties.BLOCK_SIZE * Properties.STAGE_WIDTH, Properties.BLOCK_SIZE * Properties.STAGE_HEIGHT))
        menu_surface = pygame.Surface((Properties.MENU_WIDTH, Properties.BLOCK_SIZE * Properties.STAGE_HEIGHT))

        stage_border = pygame.Rect(0, 0,
            Properties.BLOCK_SIZE * Properties.STAGE_WIDTH + 2 * Properties.WINDOW_BORDER_WIDTH,
            Properties.BLOCK_SIZE * Properties.STAGE_HEIGHT + 2 * Properties.WINDOW_BORDER_WIDTH)

        menu_border = pygame.Rect(Properties.BLOCK_SIZE * Properties.STAGE_WIDTH, 0,
            Properties.MENU_WIDTH + 2 * Properties.WINDOW_BORDER_WIDTH,
            Properties.BLOCK_SIZE * Properties.STAGE_HEIGHT + 2 * Properties.WINDOW_BORDER_WIDTH)

        pygame.draw.rect(screen, Properties.BLOCK_BORDER_COLOR, stage_border, Properties.WINDOW_BORDER_WIDTH)
        pygame.draw.rect(screen, Properties.BLOCK_BORDER_COLOR, menu_border, Properties.WINDOW_BORDER_WIDTH)

        clock = pygame.time.Clock()
        stage = Stage()
        collision = Collision(stage)
        rotated = 0
        gravity = 0
        figure = self.get_random_figure()
        next_figure = self.get_random_figure()
        menu = Menu(stage, next_figure)

        while True:
            stage_surface.fill(Properties.BACKGROUND_COLOR)
            menu_surface.fill(Properties.BACKGROUND_COLOR)

            stage.draw(stage_surface)
            figure.draw(stage_surface)
            menu.draw(menu_surface)

            screen.blit(stage_surface, (Properties.WINDOW_BORDER_WIDTH, Properties.WINDOW_BORDER_WIDTH))
            screen.blit(menu_surface, (Properties.BLOCK_SIZE * Properties.STAGE_WIDTH + 2 * Properties.WINDOW_BORDER_WIDTH,
                                       Properties.WINDOW_BORDER_WIDTH))

            pygame.display.update()
            move_x = 0
            move_y = 0

            if collision.collision_row == 1:
                # TODO: implement Game Over
                pygame.quit()
                sys.exit(True)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(True)

            # key check
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

            # Add delay to the rotation action
            if 0 < rotated < 3:
                rotated += 1
            else:
                rotated = 0

            # More is less
            if gravity < 8:
                gravity += 1
            else:
                gravity = 0
                move_y = 1

            # First check horizontal collides, horizontal collides don't produce merges
            if collision.check_x(figure, move_x):
                move_x = 0
                print("collide with column " + str(collision.collision_column))
            figure.x += move_x

            # Finally check vertical collides, this produces merges
            if collision.check_y(figure, move_y):
                move_y = 0
                stage.merge_figure(figure)
                figure = next_figure
                next_figure = self.get_random_figure()
                menu.next_figure = next_figure
                print("merge at row " + str(collision.collision_row))
            figure.y += move_y

            # Check completed lines, remove them and add new at the beginning
            stage.check_completed_lines()

            clock.tick(10)

    @staticmethod
    def get_random_figure():
        figure = copy.copy(figure_list[random.randint(0, len(figure_list) - 1)])
        figure.x = random.randint(0, Properties.STAGE_WIDTH - 1 - figure.width)
        figure.y = 0
        return figure
