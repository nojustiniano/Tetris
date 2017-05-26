import pygame

from properties import BLOCK_BORDER_COLOR


class BlockDrawer:
    def draw(self, rect, color, screen):
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLOCK_BORDER_COLOR, rect, 1)


class GhostBlockDrawer(BlockDrawer):
    def draw(self, rect, color, screen):
        pygame.draw.rect(screen, (255, 255, 255, 40), rect)
        pygame.draw.rect(screen, (0, 0, 0, 150), rect, 1)


class WiredBlockDrawer(BlockDrawer):
    def draw(self, rect, color, screen):
        pygame.draw.rect(screen, (0, 0, 0, 200), rect, 1)
