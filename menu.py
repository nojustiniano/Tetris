import pygame

from figure import Figure
from properties import *
from stage import Stage


class Menu:
    SEPARATION = 25
    NEXT_LINE_SEPARATION = 10

    def __init__(self, stage: Stage,  next_figure: Figure):
        self.font = pygame.font.SysFont("monospace", 20)
        self.stage = stage
        self.next_figure = next_figure

    def draw(self, screen):
        score_label = self.font.render("Score", 1, MENU_FONT_COLOR)
        score_number_label = self.font.render(str(self.stage.score), 1, MENU_FONT_COLOR)
        lines_label = self.font.render("Lines", 1, MENU_FONT_COLOR)
        lines_number_label = self.font.render(str(self.stage.completed_lines), 1, MENU_FONT_COLOR)
        next_figure_label = self.font.render("Next", 1, MENU_FONT_COLOR)

        position = 10

        screen.blit(score_label, (10, position))
        position += self.SEPARATION
        screen.blit(score_number_label, (10, position))
        position += self.SEPARATION + self.NEXT_LINE_SEPARATION
        screen.blit(lines_label, (10, position))
        position += self.SEPARATION
        screen.blit(lines_number_label, (10, position))
        position += self.SEPARATION + self.NEXT_LINE_SEPARATION
        screen.blit(next_figure_label, (10, position))
        position += self.SEPARATION

        i = j = 0
        for line in self.next_figure.blocks:
            for block in line:
                if block == 1:
                    x = i * BLOCK_SIZE
                    y = j * BLOCK_SIZE
                    rect = pygame.Rect(x + 10, y + position, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(screen, self.next_figure.color, rect)
                    pygame.draw.rect(screen, BLOCK_BORDER_COLOR, rect, 1)
                i += 1
            j += 1
            i = 0
