import sys

import pygame
from pygame.locals import *

from scripts import CONST
from scripts.main.database import Db

if __name__ == "__main__":

    CONST.db = Db()

    pygame.init()

    wd, ht = pygame.display.Info().current_w, pygame.display.Info().current_h

    flags = HWSURFACE | DOUBLEBUF | HWACCEL | NOFRAME

    CONST.surface = pygame.display.set_mode((wd, ht), display=0, flags=flags)

    pygame.display.set_caption(CONST.Name)

    CONST.clock = pygame.time.Clock()
    CONST.Running = True

    try:
        while CONST.Running:
            CONST.clock.tick(CONST.Framerate)

            # Update frame behind background
            CONST.surface.fill((0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    CONST.Running = False

            pygame.display.flip()

    except Exception as e:
        pygame.quit()

    pygame.quit()
    sys.exit(0)
