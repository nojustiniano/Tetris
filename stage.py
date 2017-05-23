import random

from figure import Figure
from properties import *


class Stage(Figure):
    def __init__(self):
        self.score = 0
        self.completed_lines = 0
        self.NEW_LINE = [0 for x in range(STAGE_WIDTH)]
        super().__init__([list(self.NEW_LINE) for y in range(STAGE_HEIGHT)])

    def merge_figure(self, figure: Figure):
        x = figure.x
        y = figure.y

        for line in figure.blocks:
            for block in line:
                if block == 1:
                    self.blocks[y][x] = block
                x += 1
            y += 1
            x = figure.x

    def remove_line(self, line):
        self.blocks.remove(line)
        self.blocks.insert(0, list(self.NEW_LINE))

    def check_completed_lines(self):
        partial_lines = 0
        for line in self.blocks:
            count = 0
            for block in line:
                count += block
            if count == STAGE_WIDTH:
                partial_lines += 1
                self.remove_line(line)
        if partial_lines > 0:
            self.score += sum([10 * n for n in range(partial_lines+1)])
            self.completed_lines += partial_lines
            print("Score: " + str(self.score) + " - Lines: " + str(self.completed_lines))

        return partial_lines

    def add_attack_line(self):
        self.blocks.remove(self.blocks[0])
        attack_line = list()
        for x in range(STAGE_WIDTH):
            attack_line.append(random.randint(0, 1))
        self.blocks.insert(0, attack_line)
