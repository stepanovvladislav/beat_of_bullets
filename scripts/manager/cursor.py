import time

import pygame

from scripts import CONST
from scripts.main import helper
from scripts.main.data import *
from scripts.main.pygameElements import PygameSprite


# noinspection PyPep8Naming
class CursorManager:
    def __init__(self):
        self.sprite = PygameSprite("cursor.png", vector2(0, 0),
                                   SkinSource.user, Positions.topLeft,
                                   Positions.topLeft)

        self.additive = PygameSprite("cursor-additive.png", vector2(0, 0),
                                     SkinSource.user, Positions.topLeft,
                                     Positions.topLeft, Color(79, 126, 255))

        self.sprite.VectorScale(vector2(0.1, 0.1))
        self.additive.VectorScale(vector2(0.1, 0.1))

    def draw(self):
        self.additive.draw()
        self.sprite.draw()
        if not CONST.Afk:
            self.additive.Fade(helper.getSyncValue(1, 0.5))

    def onClick(self):
        self.sprite.ScaleTo(1.2, 100)
        self.additive.ScaleTo(1.2, 100)
        CONST.LastActive = time.time() * 1000
        isClicked = False
        for sprite in CONST.overlaySprites.sprites:
            if sprite.isonHover:
                isClicked = True
                sprite.__onClick__()

        if not isClicked:
            for sprite in CONST.foregroundSprites.sprites:
                if sprite.isonHover:
                    sprite.__onClick__()

    def onRelease(self):
        self.sprite.ScaleTo(1, 100)
        self.additive.ScaleTo(1, 100)

    def updateCursorPos(self):
        x, y = pygame.mouse.get_pos()
        self.sprite.position = vector2(x / CONST.windowManager.getPixelSize(),
                                       y / CONST.windowManager.getPixelSize())
        self.additive.position = vector2(
            x / CONST.windowManager.getPixelSize(),
            y / CONST.windowManager.getPixelSize())
        CONST.cursorPos = vector2(x, y)
        if (time.time() * 1000) - CONST.LastActive > 6000 and not CONST.Afk:
            CONST.Afk = True
            self.sprite.FadeTo(0, 300)
            self.additive.FadeTo(0, 300)
        elif CONST.Afk and (time.time() * 1000) - CONST.LastActive < 6000:
            CONST.Afk = False
            self.sprite.FadeTo(1, 100)
