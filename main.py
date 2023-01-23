########################################################
# Main game script, used to be run within nothing else #
########################################################
import ctypes
import sys
import time
import traceback

import pygame
from pygame.locals import *

from scripts import CONST
from scripts.config import Config
from scripts.main import helper, error
from scripts.main.data import *
from scripts.main.database import Db
from scripts.main.log import Log
from scripts.main.pygameElements import PygameText, PygameSprite
from scripts.main.thread import Scheduler
from scripts.manager.audio import AudioManager, AudioMeter
from scripts.manager.menu import MenuManager
from scripts.manager.cursor import CursorManager

if __name__ == "__main__":
    CONST.Config = Config()
    CONST.db = Db()

    CONST.volume = CONST.Config["volume"]
    pygame.init()
    pygame.font.init()

    wd, ht = pygame.display.Info().current_w, pygame.display.Info().current_h

    CONST.windowManager.width = wd
    CONST.windowManager.height = ht
    CONST.windowManager.heightScaled = ht / CONST.windowManager.getPixelSize()
    CONST.windowManager.widthScaled = wd / CONST.windowManager.getPixelSize()
    print(CONST.windowManager.heightScaled, CONST.windowManager.widthScaled)
    CONST.Scheduler = Scheduler()

    flags = HWSURFACE | DOUBLEBUF | HWACCEL | NOFRAME
    CONST.surface = pygame.display.set_mode(
        (CONST.windowManager.width, CONST.windowManager.height), display=0,
        flags=flags)
    pygame.display.set_caption(CONST.Name)

    CONST.Logger = Log()

    CONST.AudioManager = AudioManager()
    CONST.MenuManager = MenuManager()

    Background = PygameSprite("background.png", vector2(0, 0),
                              SkinSource.local,
                              Positions.centre, Positions.centre)
    backgroundScale = CONST.windowManager.width / Background.image.get_width()
    Background.Scale(backgroundScale * 1.3)  # for the parralax to work
    cursor = CursorManager()
    CONST.cursor = cursor

    CONST.backgroundSprites.add(Background)

    CONST.clock = pygame.time.Clock()
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (
        0, 0, 0, 0, 0, 0, 0,0))
    Background.posMult = -1
    Background.posMultY = -1
    CONST.Background = Background

    CONST.MenuManager.ChangeMenu(Menus.MainMenu)
    CONST.AudioManager.PlayMusic("/data/files/intro")

    CONST.LastActive = time.time() * 1000

    CONST.AudioMeter = AudioMeter()

    fpsCounterBg = PygameSprite(CONST.PixelWhite, vector2(0, 0),
                                SkinSource.local,
                                Positions.bottomRight, Positions.bottomRight,
                                Color(0, 0, 0))
    fpsCounterBg.VectorScale(vector2(200, 30))
    fpsCounterBg.borderBounds(10)
    fpsCounterBg.Fade(0)
    fpsCounter = PygameText("", 25, FontStyle.thin, vector2(30, 10),
                            Positions.bottomRight, Positions.bottomRight)
    lastFpsSpike = time.time() * 1000
    timeSpike = False
    CONST.overlaySprites.add(fpsCounterBg)
    CONST.overlaySprites.add(fpsCounter)

    CONST.Running = True
    CONST.Logger.write("Initialised")
    try:
        while CONST.Running:
            CONST.clock.tick(CONST.Framerate)

            if timeSpike:
                if CONST.clock.get_fps() > CONST.Framerate - 5:
                    fpsCounter.Color(Color(255, 255, 255))
                elif CONST.clock.get_fps() > CONST.Framerate / 2:
                    fpsCounter.Color(Color(255, 123, 0))
                else:
                    fpsCounter.Color(Color(255, 0, 0))
                fpsCounter.Text(
                    "Framerate : {}/{}".format(int(CONST.clock.get_fps()),
                                               CONST.Framerate))
            if CONST.clock.get_fps() < CONST.Framerate - 5:
                lastFpsSpike = time.time() * 1000
                if not timeSpike:
                    timeSpike = True
                    fpsCounterBg.FadeTo(0.7, 500)
                    fpsCounter.FadeTo(1, 500)
            if timeSpike and time.time() * 1000 - lastFpsSpike > 5000:
                fpsCounter.FadeTo(0, 500)
                fpsCounterBg.FadeTo(0, 500)
                timeSpike = False

            CONST.surface.fill((0, 0, 0))
            CONST.AudioMeter.Update()
            cursor.updateCursorPos()
            CONST.backgroundSprites.Position(helper.SetParalax(50).x,
                                             helper.SetParalax(50).y)

            events = pygame.event.get()
            CONST.MenuManager.HandleEvents(events)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in (1, 2, 3):
                        cursor.onClick()
                    if event.button == 4:
                        CONST.AudioMeter.ChangeVolume(True)
                    if event.button == 5:
                        CONST.AudioMeter.ChangeVolume(False)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button in (1, 2, 3):
                        cursor.onRelease()
                if event.type == pygame.MOUSEMOTION:
                    CONST.LastActive = time.time() * 1000

            CONST.MenuManager.activeMenu.update()

            CONST.backgroundSprites.draw()
            CONST.foregroundSprites.draw()
            CONST.overlaySprites.draw()
            cursor.draw()

            pygame.display.flip()
    except Exception as e:
        error.raiseError(e)
        pygame.quit()
        if not CONST.Debug:
            ctypes.windll.user32.MessageBoxW(0,
                                             "BoB encountered an Error and couldn't continue Working\n\n" + traceback.format_exc() + "\n\nSee logs for further informations",
                                             "BoB - Crash", 0)

    pygame.quit()
    sys.exit(0)
