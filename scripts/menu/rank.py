import pygame
from pygame.locals import *

from scripts import CONST
from scripts.main.data import *
from scripts.main.pygameElements import PygameText, PygameSprite, PygameButton


class RankingPanel:
    def __init__(self):
        self.Transition = False
        self.disposeTime = 400
        self.data = None
        self.panel = None
        self.rank = None
        self.SoundHover = CONST.AudioManager.loadSound("button-hover.wav",
                                                       SkinSource.local)
        self.SoundClick = CONST.AudioManager.loadSound("button-select.wav",
                                                       SkinSource.local)
        self.SoundBack = CONST.AudioManager.loadSound("button-back.wav",
                                                      SkinSource.local)

    def init(self):
        CONST.Framerate = 30
        self.data = CONST.cache
        CONST.cache = None

        self.panel = PygameSprite("ranking-panel.png", vector2(0, 0),
                                  SkinSource.user, Positions.topLeft,
                                  Positions.topLeft)
        CONST.foregroundSprites.add(self.panel)
        self.panel.Scale(
            CONST.windowManager.height / self.panel.image.get_height())
        self.rank = PygameSprite(f"ranks/{(self.data['rank'])}.png",
                                 vector2(-50, 100), SkinSource.local,
                                 Positions.topRight, Positions.topRight)

        CONST.foregroundSprites.add(self.rank)

        bottomBar = PygameSprite(CONST.PixelWhite, vector2(0, 0),
                                 SkinSource.local,
                                 Positions.bottomCentre,
                                 Positions.bottomCentre, Color(50, 50, 50))
        bottomBar.VectorScale(vector2(1920, 100))
        CONST.foregroundSprites.add(bottomBar)

        button = PygameButton("Back", vector2(200, 100), FontStyle.regular,
                              vector2(100,
                                      CONST.windowManager.heightScaled - 50),
                              Color(255, 120, 174))
        button.text.position = vector2(0, 20)
        button.onClick(CONST.AudioManager.play, sound=self.SoundBack)
        button.onClick(CONST.MenuManager.ChangeMenu, type=Menus.SongSelection)
        CONST.foregroundSprites.add(button)

        play_button = PygameButton("Retry", vector2(200, 100),
                                   FontStyle.regular,
                                   vector2(
                                       CONST.windowManager.widthScaled - 100,
                                       CONST.windowManager.heightScaled - 50),
                                   Color(52, 237, 132))
        play_button.text.position = vector2(-10, 20)
        play_button.onClick(CONST.AudioManager.play, sound=self.SoundClick)
        play_button.onClick(CONST.MenuManager.ChangeMenu, type=Menus.Playing)
        CONST.foregroundSprites.add(play_button)

        stat = PygameText(CONST.AudioManager.currentSong["name"] + " [" +
                          ["normal", "hard", "insane"][CONST.Difficulty] + "]",
                          60,
                          FontStyle.thin, vector2(0, 0), Positions.topRight,
                          Positions.topRight)
        CONST.foregroundSprites.add(stat)

        stat = PygameText(str(self.data["score"]), 80, FontStyle.regular,
                          vector2(350, 17), Positions.topLeft,
                          Positions.topCentre)
        CONST.foregroundSprites.add(stat)

        stat = PygameText(str(self.data["xmgpRatio"][3]), 60,
                          FontStyle.regular,
                          vector2(200, 130), Positions.topLeft,
                          Positions.topCentre)
        CONST.foregroundSprites.add(stat)

        stat = PygameText(str(self.data["xmgpRatio"][2]), 60,
                          FontStyle.regular,
                          vector2(200, 220), Positions.topLeft,
                          Positions.topCentre)
        CONST.foregroundSprites.add(stat)

        stat = PygameText(str(self.data["xmgpRatio"][1]), 60,
                          FontStyle.regular,
                          vector2(200, 310), Positions.topLeft,
                          Positions.topCentre)
        CONST.foregroundSprites.add(stat)

        stat = PygameText(str(self.data["xmgpRatio"][0]), 60,
                          FontStyle.regular,
                          vector2(500, 310), Positions.topLeft,
                          Positions.topCentre)
        CONST.foregroundSprites.add(stat)

        stat = PygameText(str(self.data["combo"]) + "x", 60, FontStyle.regular,
                          vector2(100, 405), Positions.topLeft,
                          Positions.topCentre)
        CONST.foregroundSprites.add(stat)

        stat = PygameText(str(self.data["accuracy"]) + "%", 60,
                          FontStyle.regular,
                          vector2(380, 405), Positions.topLeft,
                          Positions.topCentre)
        CONST.foregroundSprites.add(stat)

        stat = PygameText(
            f"UR : {(self.data['unstableRate'][0][0])}ms /{(self.data['unstableRate'][0][1])}ms /{(self.data['unstableRate'][0][2])}ms",
            40, FontStyle.regular, vector2(500, 135), Positions.topLeft,
            Positions.topCentre)
        CONST.foregroundSprites.add(stat)

        bg = PygameSprite(CONST.PixelWhite, vector2(-100, 395),
                          SkinSource.local,
                          Positions.topCentre,
                          Positions.topCentre, Color(0, 0, 0))
        bg.VectorScale(vector2(300, 55))
        bg.Fade(0.7)
        CONST.foregroundSprites.add(bg)

        perfectLine = PygameSprite(CONST.PixelWhite, vector2(-100, 420),
                                   SkinSource.local, Positions.topCentre,
                                   Positions.topCentre, Color(56, 185, 255))
        perfectLine.VectorScale(vector2(100, 5))
        CONST.foregroundSprites.add(perfectLine)

        goodLine = PygameSprite(CONST.PixelWhite, vector2(-150, 420),
                                SkinSource.local, Positions.topCentre,
                                Positions.topRight, Color(56, 255, 86))
        goodLine.VectorScale(vector2(50, 5))
        CONST.foregroundSprites.add(goodLine)

        goodLine = PygameSprite(CONST.PixelWhite, vector2(-50, 420),
                                SkinSource.local, Positions.topCentre,
                                Positions.topLeft, Color(56, 255, 86))
        goodLine.VectorScale(vector2(50, 5))
        CONST.foregroundSprites.add(goodLine)

        MehLine = PygameSprite(CONST.PixelWhite, vector2(-199, 420),
                               SkinSource.local, Positions.topCentre,
                               Positions.topRight, Color(255, 142, 77))
        MehLine.VectorScale(vector2(50, 5))
        CONST.foregroundSprites.add(MehLine)

        MehLine = PygameSprite(CONST.PixelWhite, vector2(-1, 420),
                               SkinSource.local,
                               Positions.topCentre,
                               Positions.topLeft, Color(255, 142, 77))
        MehLine.VectorScale(vector2(50, 5))
        CONST.foregroundSprites.add(MehLine)

        lines = self.data["unstableRate"][1]
        CONST.Logger.debug(lines)

        offset = (self.data["mapOD"]) / 290

        for line in lines:
            positionX = -100 + (line * offset)
            lSprite = PygameSprite(CONST.PixelWhite, vector2(positionX, 422.5),
                                   SkinSource.local, Positions.topCentre,
                                   Positions.centre)
            lSprite.VectorScale(vector2(2, 55))
            lSprite.Fade(0.2)
            CONST.foregroundSprites.add(lSprite)

    def HandleEvents(self, events):
        keys = pygame.key.get_pressed()

        if keys[K_ESCAPE]:
            CONST.MenuManager.ChangeMenu(Menus.SongSelection)

        for event in events:
            if event.type == CONST.UserEvents["MUSIC_END"]:
                CONST.AudioManager.SeekPreview()
                CONST.AudioManager.Pause()
            if event.type == pygame.QUIT:
                CONST.MenuManager.ChangeMenu(Menus.SongSelection)
