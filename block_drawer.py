import pygame

from properties import BLOCK_BORDER_COLOR


class BlockDrawer:
    def draw(self, rect, color, screen):
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLOCK_BORDER_COLOR, rect, 1)


class GhostBlockDrawer(BlockDrawer):
    def draw(self, rect, color, screen):
        pygame.draw.rect(screen, (255, 255, 255, 20), rect)
        pygame.draw.rect(screen, (255, 255, 255, 40), rect, 1)
