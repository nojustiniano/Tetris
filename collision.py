from figure import Figure
from properties import *


class Collision:
    def __init__(self, stage: Figure):
        self.stage = stage
        self.collision_column = 0
        self.collision_row = 0

    def check_x(self, figure: Figure, move_x):
        self.collision_column = 0

        if figure.x + move_x < 0:
            self.collision_column = 0
            return True
        elif figure.x + move_x + figure.width > STAGE_WIDTH:
            self.collision_column = STAGE_WIDTH
            return True
        else:
            x = figure.x
            y = figure.y
            for line in figure.blocks:
                for block in line:
                    if block == 1 and self.stage.blocks[y][x + move_x] == 1:
                        self.collision_column = x + move_x
                        return True
                    x += 1
                y += 1
                x = figure.x

        return False

    def check_y(self, figure: Figure, move_y):
        self.collision_row = 0

        if figure.y + figure.height + move_y > STAGE_HEIGHT:
            self.collision_row = figure.y + figure.height + move_y
            return True
        else:
            x = figure.x
            y = figure.y
            for line in figure.blocks:
                for block in line:
                    if block == 1 and self.stage.blocks[y+move_y][x] == 1:
                        self.collision_row = y + move_y
                        return True
                    x += 1
                y += 1
                x = figure.x

        return False
