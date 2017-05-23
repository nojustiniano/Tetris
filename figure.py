import pygame

from block_drawer import BlockDrawer
from properties import *


class Figure:
    def __init__(self, blocks, color=(0, 80, 150)):
        self.blocks = blocks
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self._calculate_size()
        self.color = color
        self.block_drawer = BlockDrawer()

    def rotate_right(self):
        self.blocks = list(zip(*self.blocks[::-1]))
        self._calculate_size()
        # Prevents the figure from leaving the stage
        if self.x + self.width > STAGE_WIDTH:
            self.x -= self.x + self.width - STAGE_WIDTH

    def rotate_left(self):
        self.blocks = list(reversed(list(zip(*self.blocks))))
        self._calculate_size()

    def draw(self, screen):
        i = j = 0
        for line in self.blocks:
            for block in line:
                if block == 1:
                    x = (i + self.x) * BLOCK_SIZE
                    y = (j + self.y) * BLOCK_SIZE
                    rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                    self.block_drawer.draw(rect, self.color, screen)
                i += 1
            j += 1
            i = 0

    # Calculate the figure height and with, if the figure rotate you need to calculate again
    def _calculate_size(self):
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


i_figure = Figure([[1, 1, 1, 1]], (200, 0, 0))
j_figure = Figure([[1, 1, 1],
                   [0, 0, 1]], (180, 180, 0))
l_figure = Figure([[1, 1, 1],
                   [1, 0, 0]], (180, 0, 180))
o_figure = Figure([[1, 1],
                   [1, 1]], (0, 0, 200))
s_figure = Figure([[0, 1, 1],
                   [1, 1, 0]], (0, 150, 150))
t_figure = Figure([[1, 1, 1],
                   [0, 1, 0]], (0, 180, 0))
z_figure = Figure([[1, 1, 0],
                   [0, 1, 1]], (220, 130, 50))
figure_list = [i_figure, j_figure, l_figure, o_figure, s_figure, t_figure, z_figure]
