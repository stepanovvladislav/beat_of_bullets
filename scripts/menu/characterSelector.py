import pygame
from pygame.locals import *

from scripts import CONST
from scripts.main import helper
from scripts.main.data import *
from scripts.main.pygameElements import PygameButton, PygameSprite


class CharacterSelector:

    def __init__(self):
        self.Playbutton = None
        self.playEnemy1 = None
        self.playEnemy2 = None
        self.playEnemy3 = None
        self.background = None
        self.logoEnemy1 = None
        self.logoEnemy2 = None
        self.logoEnemy3 = None
        self.upperBar = None
        self.lowerBar = None

        self.SoundHover = CONST.AudioManager.loadSound("button-hover.wav",
                                                       SkinSource.local)
        self.SoundClick = CONST.AudioManager.loadSound("button-select.wav",
                                                       SkinSource.local)

    def init(self):
        CONST.Framerate = 30

        upperBar = PygameSprite(CONST.PixelWhite, vector2(0, 0),
                                SkinSource.local,
                                Positions.topCentre, Positions.topCentre,
                                Color(50, 50, 50))
        upperBar.VectorScale(vector2(1920, 50))
        self.upperBar = upperBar
        CONST.foregroundSprites.add(upperBar)

        bottomBar = PygameSprite(CONST.PixelWhite, vector2(0, 0),
                                 SkinSource.local,
                                 Positions.bottomCentre,
                                 Positions.bottomCentre,
                                 Color(50, 50, 50))
        bottomBar.VectorScale(vector2(1920, 50))
        CONST.foregroundSprites.add(bottomBar)
        self.lowerBar = bottomBar

        LogoEnemy1 = PygameSprite("logo-hero.png", vector2(350, -50),
                                  SkinSource.user,
                                  Positions.centreLeft, Positions.centre)
        self.logoEnemy1 = LogoEnemy1
        CONST.foregroundSprites.add(LogoEnemy1)

        LogoEnemy2 = PygameSprite("logo-hero.png", vector2(0, -50),
                                  SkinSource.user,
                                  Positions.centre, Positions.centre)
        self.logoEnemy2 = LogoEnemy2
        CONST.foregroundSprites.add(LogoEnemy2)

        LogoEnemy3 = PygameSprite("logo-hero.png", vector2(-250, -50),
                                  SkinSource.user,
                                  Positions.centreRight, Positions.centre)
        self.logoEnemy3 = LogoEnemy3
        CONST.foregroundSprites.add(LogoEnemy3)

        PlayEnemy1 = PygameButton("Play", vector2(400, 150),
                                  position=vector2(400, 950),
                                  color=Color(82, 2, 105))
        self.playEnemy1 = PlayEnemy1
        self.playEnemy1.onHover(CONST.AudioManager.play, sound=self.SoundHover)
        CONST.foregroundSprites.add(PlayEnemy1)
        CONST.enemy = '1'
        self.playEnemy1.onClick(CONST.MenuManager.ChangeMenu,
                                type=Menus.SongSelection)

        PlayEnemy2 = PygameButton("Play2", vector2(400, 150),
                                  position=vector2(950, 950),
                                  color=Color(82, 2, 105))
        self.playEnemy2 = PlayEnemy2
        self.playEnemy2.onHover(CONST.AudioManager.play, sound=self.SoundHover)
        CONST.foregroundSprites.add(PlayEnemy2)
        CONST.enemy = '2'
        self.playEnemy2.onClick(CONST.MenuManager.ChangeMenu,
                                type=Menus.SongSelection)

        PlayEnemy3 = PygameButton("Play3", vector2(400, 150),
                                  position=vector2(1550, 950),
                                  color=Color(82, 2, 105))
        self.playEnemy3 = PlayEnemy3
        self.playEnemy3.onHover(CONST.AudioManager.play, sound=self.SoundHover)
        CONST.foregroundSprites.add(PlayEnemy3)
        CONST.enemy = '3'
        self.playEnemy3.onClick(CONST.MenuManager.ChangeMenu,
                                type=Menus.SongSelection)

    def update(self):
        self.logoEnemy1.position = helper.SetParalax(40)
        self.logoEnemy1.Scale(
            helper.getSyncValue(0.99, 1, EaseTypes.easeOut))
        self.logoEnemy1.Rotate(
            helper.getSyncValue(-3, 3, EaseTypes.easeInOut))
        self.logoEnemy1.Rotate(
            helper.getSyncValue(3, -3, EaseTypes.easeInOut))
        self.logoEnemy1.Scale(self.logoEnemy1.scale)
        self.logoEnemy1.posMultY = 1
        self.logoEnemy1.posMult = 1

        self.logoEnemy2.position = helper.SetParalax(40)
        self.logoEnemy2.Scale(
            helper.getSyncValue(0.99, 1, EaseTypes.easeOut))
        self.logoEnemy2.Rotate(
            helper.getSyncValue(-3, 3, EaseTypes.easeInOut))
        self.logoEnemy2.Rotate(
            helper.getSyncValue(3, -3, EaseTypes.easeInOut))
        self.logoEnemy2.Scale(self.logoEnemy2.scale)
        self.logoEnemy2.posMultY = 1
        self.logoEnemy2.posMult = 1

        self.logoEnemy3.position = helper.SetParalax(40)
        self.logoEnemy3.Scale(
            helper.getSyncValue(0.99, 1, EaseTypes.easeOut))
        self.logoEnemy3.Rotate(
            helper.getSyncValue(-3, 3, EaseTypes.easeInOut))
        self.logoEnemy3.Rotate(
            helper.getSyncValue(3, -3, EaseTypes.easeInOut))
        self.logoEnemy3.Scale(self.logoEnemy3.scale)
        self.logoEnemy3.posMultY = 1
        self.logoEnemy3.posMult = 1

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                helper.GameQuit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 2):
                    self.isMouseDown = True
                if event.button == 4:
                    CONST.AudioMeter.ChangeVolume(True)
                if event.button == 5:
                    CONST.AudioMeter.ChangeVolume(False)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 2):
                    self.isMouseDown = False

    def dispose(self):
        for sprite in CONST.foregroundSprites.sprites:
            sprite.FadeTo(0, 400)
