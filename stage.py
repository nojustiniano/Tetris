from tetris.figure import Figure
from tetris.properties import Properties


class Stage(Figure):
    def __init__(self):
        super().__init__([[0 for x in range(Properties.STAGE_WIDTH)] for y in range(Properties.STAGE_HEIGHT)])

    def merge_figure(self, figure: Figure):
        x = figure.position.x
        y = figure.position.y

        for line in figure.blocks:
            for block in line:
                if block == 1:
                    self.blocks[y][x] = block
                x += 1
            y += 1
            x = figure.position.x
