import pygame

from tetris.position import Position
from tetris.properties import Properties


class Figure:
    BLOCK_SIZE = Properties.BLOCK_SIZE

    def __init__(self, blocks):
        self.blocks = blocks
        self.position = Position(0, 0)
        self.width = 0
        self.height = 0
        self.calculate_size()

    def rotate_right(self):
        self.blocks = list(zip(*self.blocks[::-1]))
        self.calculate_size()

    def rotate_left(self):
        self.blocks = list(reversed(list(zip(*self.blocks))))
        self.calculate_size()

    def draw(self, screen):
        i = j = 0
        for line in self.blocks:
            for block in line:
                if block == 1:
                    x = (i + self.position.x) * self.BLOCK_SIZE
                    y = (j + self.position.y) * self.BLOCK_SIZE
                    pygame.draw.rect(screen, (0, 150, 80), pygame.Rect(x, y, self.BLOCK_SIZE, self.BLOCK_SIZE))
                i += 1
            j += 1
            i = 0

    def calculate_size(self):
        self.width = 1
        self.height = 1
        i = 1
        j = 1
        for line in self.blocks:
            for block in line:
                if block == 1 and i > self.width:
                    self.width = i
                i += 1
            if j > self.height:
                self.height = j
            j += 1
            i = 1


i_figure = Figure([[1, 1, 1, 1]])
j_figure = Figure([[1, 1, 1],
                   [0, 0, 1]])
l_figure = Figure([[1, 1, 1],
                   [1, 0, 0]])
o_figure = Figure([[1, 1],
                   [1, 1]])
s_figure = Figure([[0, 1, 1],
                   [1, 1, 0]])
t_figure = Figure([[1, 1, 1],
                   [0, 1, 0]])
z_figure = Figure([[1, 1, 0],
                   [0, 1, 1]])
