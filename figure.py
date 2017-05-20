import pygame

from properties import Properties


class Figure:
    BLOCK_SIZE = Properties.BLOCK_SIZE

    def __init__(self, blocks, color=(0, 80, 150)):
        self.blocks = blocks
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.calculate_size()
        self.color = color

    def rotate_right(self):
        self.blocks = list(zip(*self.blocks[::-1]))
        self.calculate_size()
        if self.x + self.width > Properties.STAGE_WIDTH:
            self.x -= self.x + self.width - Properties.STAGE_WIDTH

    def rotate_left(self):
        self.blocks = list(reversed(list(zip(*self.blocks))))
        self.calculate_size()

    def draw(self, screen):
        i = j = 0
        for line in self.blocks:
            for block in line:
                if block == 1:
                    x = (i + self.x) * self.BLOCK_SIZE
                    y = (j + self.y) * self.BLOCK_SIZE
                    pygame.draw.rect(screen, self.color, pygame.Rect(x, y, self.BLOCK_SIZE, self.BLOCK_SIZE))
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


i_figure = Figure([[1, 1, 1, 1]], (255, 0, 0))
j_figure = Figure([[1, 1, 1],
                   [0, 0, 1]], (255, 255, 0))
l_figure = Figure([[1, 1, 1],
                   [1, 0, 0]], (255, 0, 255))
o_figure = Figure([[1, 1],
                   [1, 1]], (0, 0, 255))
s_figure = Figure([[0, 1, 1],
                   [1, 1, 0]], (0, 255, 255))
t_figure = Figure([[1, 1, 1],
                   [0, 1, 0]], (0, 255, 0))
z_figure = Figure([[1, 1, 0],
                   [0, 1, 1]], (255, 153, 51))
figure_list = [i_figure, j_figure, l_figure, o_figure, s_figure, t_figure, z_figure]
