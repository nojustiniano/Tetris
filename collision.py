from tetris.figure import Figure
from tetris.properties import Properties


class Collision:
    BLOCK_SIZE = Properties.BLOCK_SIZE
    STAGE_HEIGHT = Properties.STAGE_HEIGHT
    STAGE_WIDTH = Properties.STAGE_WIDTH

    def __init__(self, stage: Figure):
        self.stage = stage

    def check_borders(self, figure: Figure, move_x):
        result = False
        if figure.position.x + move_x < 0 or figure.position.x + move_x + figure.width > self.STAGE_WIDTH:
            result = True

        return result

    def check_stage(self, figure: Figure, move_x, move_y):

        if figure.position.y + figure.height + move_y > self.STAGE_HEIGHT:
            return True
        else:
            x = figure.position.x
            y = figure.position.y
            for line in figure.blocks:
                for block in line:
                    if block == 1 and self.stage.blocks[y+move_y][x+move_x] == 1:
                        return True
                    x += 1
                y += 1
                x = figure.position.x

        return False
