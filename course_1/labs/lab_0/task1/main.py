__all__ = []

import pygame

from objects import Game
from settings import DISPLAY_RESOLUTION, FRAMERATE


def main():
    screen = pygame.display.set_mode(DISPLAY_RESOLUTION, pygame.SRCALPHA)
    game = Game(screen, FRAMERATE)
    game.start()


if __name__ == "__main__":
    main()
