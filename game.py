import copy
import random
import pygame
import sys
from pygame.locals import *

from properties import *
from collision import Collision
from figure import figure_list
from menu import Menu
from secondplayer import NoPlayer, LanSecondPlayer
from stage import Stage


class Game:
    def __init__(self, lan):
        pygame.init()
        self.gravity = 0
        self.rotated = 0
        self.next_figure = self.get_random_figure()
        self.figure = self.get_random_figure()
        self.stage = Stage()
        self.menu = Menu(self.stage, self.next_figure)
        self.collision = Collision(self.stage)
        self.move_x = 0
        self.move_y = 0
        if lan is None:
            self.second_player = NoPlayer()
        else:
            self.second_player = LanSecondPlayer(self.menu, lan)

    def start_game(self):
        pygame.display.set_caption("Tetris")

        screen = self.draw_screen()
        stage_surface = pygame.Surface((BLOCK_SIZE * STAGE_WIDTH, BLOCK_SIZE * STAGE_HEIGHT), pygame.SRCALPHA)
        second_player_stage_surface = pygame.Surface((BLOCK_SIZE * STAGE_WIDTH, BLOCK_SIZE * STAGE_HEIGHT),
                                                     pygame.SRCALPHA)
        menu_surface = pygame.Surface((MENU_WIDTH, BLOCK_SIZE * STAGE_HEIGHT))

        menu_horizontal_position = BLOCK_SIZE * STAGE_WIDTH + 2 * WINDOW_BORDER_WIDTH

        clock = pygame.time.Clock()

        while True:
            # Erase all
            stage_surface.fill(BACKGROUND_COLOR)
            second_player_stage_surface.fill((0, 0, 0, 0))
            menu_surface.fill(BACKGROUND_COLOR)
            screen.blit(stage_surface, (WINDOW_BORDER_WIDTH, WINDOW_BORDER_WIDTH))

            # Draw the stage elements
            self.stage.draw(stage_surface)
            self.figure.draw(stage_surface)
            # Draw the menu elements
            self.menu.draw(menu_surface)
            # Draw the second player things
            self.second_player.draw(second_player_stage_surface, menu_surface)

            screen.blit(stage_surface, (WINDOW_BORDER_WIDTH, WINDOW_BORDER_WIDTH))
            screen.blit(second_player_stage_surface, (WINDOW_BORDER_WIDTH, WINDOW_BORDER_WIDTH))
            screen.blit(menu_surface, (menu_horizontal_position, WINDOW_BORDER_WIDTH))
            # Update screen
            pygame.display.update()

            # Reset movement
            self.move_x = 0
            self.move_y = 0

            # If there was a collision in the first line them game over
            if self.collision.collision_row == 1:
                # TODO: implement Game Over
                pygame.quit()
                sys.exit(True)

            self.check_keys_pressed()
            self.check_collisions()
            # Check completed lines, remove them and add new at the beginning
            completed_lines = self.stage.check_completed_lines()

            # Exchange data with the second player
            attack = self.second_player.receive_data()

            if attack > 1:
                for n in range(attack - 1):
                    self.stage.add_attack_line()

            self.second_player.send_data(self.figure, self.stage, completed_lines)

            clock.tick(10)

    def draw_screen(self):
        screen = pygame.display.set_mode((
            BLOCK_SIZE * STAGE_WIDTH + MENU_WIDTH + 3 * WINDOW_BORDER_WIDTH,
            BLOCK_SIZE * STAGE_HEIGHT + 2 * WINDOW_BORDER_WIDTH
        ), pygame.DOUBLEBUF, 32)
        stage_border = pygame.Rect(0, 0, BLOCK_SIZE * STAGE_WIDTH + 2 * WINDOW_BORDER_WIDTH,
                                   BLOCK_SIZE * STAGE_HEIGHT + 2 * WINDOW_BORDER_WIDTH)
        menu_border = pygame.Rect(BLOCK_SIZE * STAGE_WIDTH, 0, MENU_WIDTH + 2 * WINDOW_BORDER_WIDTH,
                                  BLOCK_SIZE * STAGE_HEIGHT + 2 * WINDOW_BORDER_WIDTH)
        pygame.draw.rect(screen, BLOCK_BORDER_COLOR, stage_border, WINDOW_BORDER_WIDTH)
        pygame.draw.rect(screen, BLOCK_BORDER_COLOR, menu_border, WINDOW_BORDER_WIDTH)
        return screen

    def check_keys_pressed(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(True)

        # key check
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_DOWN]:
            self.move_y = 1
        if pressed[pygame.K_LEFT]:
            self.move_x = -1
        if pressed[pygame.K_RIGHT]:
            self.move_x = 1
        if pressed[pygame.K_a]:
            if self.rotated == 0:
                self.figure.rotate_left()
                self.rotated = 1
        if pressed[pygame.K_d]:
            if self.rotated == 0:
                self.figure.rotate_right()
                self.rotated = 1

        # Add delay to the rotation action
        if 0 < self.rotated < 3:
            self.rotated += 1
        else:
            self.rotated = 0

        # More is less
        if self.gravity < 8:
            self.gravity += 1
        else:
            self.gravity = 0
            self.move_y = 1

    # Checks collisions with borders and other blocks, if the figure don't collides apply the movement,
    # if collides horizontally not apply the movement and finally if collides vertically merge the
    # figure blocks with the stage and launch a new figure
    def check_collisions(self):
        # First check horizontal collides, horizontal collides don't produce merges
        if self.collision.check_x(self.figure, self.move_x):
            self.move_x = 0
            print("collide with column " + str(self.collision.collision_column))
        self.figure.x += self.move_x

        # Finally check vertical collides, this produces merges
        if self.collision.check_y(self.figure, self.move_y):
            self.move_y = 0
            self.stage.merge_figure(self.figure)
            self.figure = self.next_figure
            self.next_figure = self.get_random_figure()
            self.menu.next_figure = self.next_figure
            print("merge at row " + str(self.collision.collision_row))
        self.figure.y += self.move_y

    # It returns a random copy of a figure from figure_list
    @staticmethod
    def get_random_figure():
        figure = copy.copy(figure_list[random.randint(0, len(figure_list) - 1)])
        figure.x = random.randint(0, STAGE_WIDTH - 1 - figure.width)
        figure.y = 0
        return figure
