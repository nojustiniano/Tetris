import pygame

from figure import Figure
from properties import Properties
from stage import Stage


class Menu:
    def __init__(self, stage: Stage,  next_figure: Figure):
        self.font = pygame.font.SysFont("monospace", 20)
        self.stage = stage
        self.next_figure = next_figure

    def draw(self, screen):
        score_label = self.font.render("Score", 1, Properties.MENU_FONT_COLOR)
        score_number_label = self.font.render(str(self.stage.score), 1, Properties.MENU_FONT_COLOR)
        lines_label = self.font.render("Lines", 1, Properties.MENU_FONT_COLOR)
        lines_number_label = self.font.render(str(self.stage.completed_lines), 1, Properties.MENU_FONT_COLOR)
        next_figure_label = self.font.render("Next", 1, Properties.MENU_FONT_COLOR)

        position = 10
        separation = 25
        next_line_separation = 10

        screen.blit(score_label, (10, position))
        position += separation
        screen.blit(score_number_label, (10, position))
        position += separation + next_line_separation
        screen.blit(lines_label, (10, position))
        position += separation
        screen.blit(lines_number_label, (10, position))
        position += separation + next_line_separation
        screen.blit(next_figure_label, (10, position))
        position += separation

        i = j = 0
        for line in self.next_figure.blocks:
            for block in line:
                if block == 1:
                    x = i * Properties.BLOCK_SIZE
                    y = j * Properties.BLOCK_SIZE
                    rect = pygame.Rect(x + 10, y + position, Properties.BLOCK_SIZE, Properties.BLOCK_SIZE)
                    pygame.draw.rect(screen, self.next_figure.color, rect)
                    pygame.draw.rect(screen, Properties.BLOCK_BORDER_COLOR, rect, 1)
                i += 1
            j += 1
            i = 0
