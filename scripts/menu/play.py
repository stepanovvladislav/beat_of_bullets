import pygame
from pygame.locals import *

from scripts import CONST
from scripts.main import helper
from scripts.main import error
from scripts.main.data import *
from scripts.main.pygameElements import PygameNotification, NotificationMassive
from scripts.main.pygameElements import PygameSprite, PygameText, PygameNote
from scripts.main.pygameElements import PygameButton


class Gameplay:
    def __init__(self):

        self.ScoreIndicator = None
        self.LengthTime = None
        self.failOverlay = None
        self.failRetry = None
        self.failQuit = None
        self.Loading = None
        self.UpperSprite = None
        self.LowerSprite = None
        self.upperOv = None
        self.lowerOv = None
        self.accBar = None
        self.progressBar = None
        self.lifeBar = None
        self.healthBar = None
        self.comboIndicator = None
        self.comboIndicatorOv = None

        self.touchSound = CONST.AudioManager.loadSound("play-touch.mp3",
                                                       SkinSource.user)
        self.hitSound = CONST.AudioManager.loadSound("play-hit.mp3",
                                                     SkinSource.user)
        self.failSound = CONST.AudioManager.loadSound("failsound.mp3",
                                                      SkinSource.user)
        self.SoundHover = CONST.AudioManager.loadSound("button-hover.wav",
                                                       SkinSource.local)
        self.SoundClick = CONST.AudioManager.loadSound("button-select.wav",
                                                       SkinSource.local)

        self.isLoading = True
        self.key1Holt = False
        self.key2Holt = False
        self.failed = False
        self.finished = False
        self.Transition = False
        self.paused = False

        self.fileBody = ""

        self.life = 100
        self.disposeTime = 400
        self.ClosingTime = 0
        self.score = 0
        self.combo = 0
        self.maxCombo = 0
        self.hp = 0
        self.ar = 0
        self.od = 0

        self.unstableRate = []
        self.accList = []
        self.upperSprites = []
        self.lowerSprites = []

    def init(self):

        CONST.Framerate = 30

        CONST.AudioManager.Restart()
        CONST.AudioManager.Pause()

        difficulties = {Difficulty.Normal: "normal.dd",
                        Difficulty.Hard: "hard.dd",
                        Difficulty.Insane: "insane.dd"}

        difficulty = difficulties[CONST.Difficulty]
        with open(CONST.AudioManager.currentSong[
                      "folder"] + "/" + difficulty) as f:
            file = f.read()
            data = file.split("\n")[0].split("|")
            self.fileBody = file.split("\n")[1:]

            if len(self.fileBody) == 0:
                CONST.MenuManager.ChangeMenu(type=Menus.SongSelection)
                NotificationMassive(text="Beatmap is empty", duration=5000,
                                    type=NotificationType.Error).show()
                return

        self.hp = (float(data[1]) + 1) * 10
        self.ar = 1 / (1 + float(data[2])) * 3000

        self.od = 1 / (1 + float(data[3]) / 3) * 200

        CONST.backgroundSprites.sprites[0].FadeTo(0.1, 400)

        accBar = PygameSprite(CONST.PixelWhite, vector2(0, 0),
                              SkinSource.local,
                              Positions.centre, Positions.centre,
                              Color(0, 246, 226))

        accBar.Fade(0.5)
        accBar.VectorScale(vector2(5, CONST.windowManager.heightScaled))

        self.accBar = accBar
        CONST.foregroundSprites.add(accBar)

        lowerStruct = PygameSprite("gameplay-struct.png", vector2(0, 0),
                                   SkinSource.user, Positions.bottomCentre,
                                   Positions.bottomCentre)

        lowerStruct.Scale(0.8)

        CONST.foregroundSprites.add(lowerStruct)

        upperStruct = PygameSprite("gameplay-struct.png", vector2(0, 0),
                                   SkinSource.user, Positions.topCentre,
                                   Positions.topCentre)
        upperStruct.Scale(0.8)
        upperStruct.Rotate(180)

        upperStruct.Color(Color(176, 156, 255))
        lowerStruct.Color(Color(255, 153, 153))

        self.Loading = PygameText("Beatmap is Loading", 60, FontStyle.bold,
                                  vector2(0, 0), Positions.topCentre,
                                  Positions.topCentre)
        self.Loading.FadeTo(0.5, 2000, EaseTypes.easeInOut, True)

        self.lowerOv = PygameSprite("gameplay-struct-ov.png", vector2(0, 0),
                                    SkinSource.user, Positions.bottomCentre,
                                    Positions.bottomCentre)
        self.lowerOv.Scale(0.8)
        self.lowerOv.Fade(0)

        self.upperOv = PygameSprite("gameplay-struct-ov.png", vector2(0, 0),
                                    SkinSource.user, Positions.topCentre,
                                    Positions.topCentre)
        self.upperOv.Scale(0.8)
        self.upperOv.Fade(0)

        CONST.foregroundSprites.add(upperStruct)

        self.progressBar = PygameSprite(CONST.PixelWhite, vector2(0, 0),
                                        SkinSource.local, Positions.bottomLeft,
                                        Positions.bottomLeft)
        CONST.foregroundSprites.add(self.progressBar)
        self.progressBar.VectorScale(vector2(0, 5))
        self.LengthTime = PygameText("00:00", 40, FontStyle.regular,
                                     vector2(0, 10),
                                     Positions.bottomLeft,
                                     Positions.bottomLeft)
        CONST.foregroundSprites.add(self.LengthTime)
        seconds = str(
            int((CONST.AudioManager.currentSong["length"] / 1000) % 60))
        if len(seconds) == 1:
            seconds = "0" + seconds
        minutes = str(
            int((CONST.AudioManager.currentSong["length"] / 1000 / 60) % 60))

        totalLength = PygameText("{}:{}".format(minutes, seconds), 40,
                                 FontStyle.regular, vector2(0, 10),
                                 Positions.bottomRight, Positions.bottomRight)
        CONST.foregroundSprites.add(totalLength)

        self.upperSprites.sort(key=lambda x: x.time)

        self.comboIndicator = PygameText("0x", 100, FontStyle.regular,
                                         vector2(0, 0), Positions.centre,
                                         Positions.centre)

        self.comboIndicatorOv = PygameText("0x", 100, FontStyle.regular,
                                           vector2(0, 0), Positions.centre,
                                           Positions.centre)

        self.ScoreIndicator = PygameText("0", 50, FontStyle.regular,
                                         vector2(10, 0),
                                         Positions.topRight,
                                         Positions.topRight)

        self.lifeBar = PygameSprite(CONST.PixelWhite, vector2(0, 0),
                                    SkinSource.local, Positions.topLeft,
                                    Positions.topLeft)

        self.lifeBar.VectorScale(vector2(1920, 5))

        CONST.foregroundSprites.add(self.comboIndicator)
        CONST.foregroundSprites.add(self.comboIndicatorOv)
        CONST.foregroundSprites.add(self.ScoreIndicator)
        CONST.foregroundSprites.add(self.lifeBar)

        CONST.foregroundSprites.add(self.upperOv)
        CONST.foregroundSprites.add(self.lowerOv)

        self.failOverlay = PygameSprite("fail-background.png", vector2(0, 0),
                                        SkinSource.user, Positions.centre,
                                        Positions.centre)
        self.failOverlay.Scale(
            CONST.windowManager.width / self.failOverlay.image.get_width())
        self.failOverlay.Fade(0)
        CONST.foregroundSprites.add(self.failOverlay)

        self.failRetry = PygameSprite("fail-retry.png", vector2(0, 30),
                                      SkinSource.user, Positions.centre,
                                      Positions.centre)
        self.failRetry.Scale(0.7)
        self.failRetry.Fade(0)

        self.failRetry.onHover(self.failRetry.ScaleTo, scale=0.75,
                               duration=200)
        self.failRetry.onHover(CONST.AudioManager.play, sound=self.SoundHover)
        self.failRetry.onClick(CONST.AudioManager.play, sound=self.SoundClick)
        self.failRetry.onClick(CONST.MenuManager.ChangeMenu,
                               type=Menus.Playing)
        self.failRetry.onHoverLost(self.failRetry.ScaleTo, scale=0.7,
                                   duration=200)

        self.failRetry.enabled = False
        CONST.foregroundSprites.add(self.failRetry)

        self.failQuit = PygameSprite("fail-back.png", vector2(0, 260),
                                     SkinSource.user, Positions.centre,
                                     Positions.centre)
        self.failQuit.Fade(0)
        self.failQuit.Scale(0.7)

        self.failQuit.onHover(self.failQuit.ScaleTo, scale=0.75, duration=200)
        self.failQuit.onHover(CONST.AudioManager.play, sound=self.SoundHover)
        self.failQuit.onClick(CONST.AudioManager.play, sound=self.SoundClick)
        self.failQuit.onClick(CONST.MenuManager.ChangeMenu,
                              type=Menus.SongSelection)
        self.failQuit.onHoverLost(self.failQuit.ScaleTo, scale=0.7,
                                  duration=200)

        self.failQuit.enabled = False
        CONST.foregroundSprites.add(self.failQuit)
        CONST.foregroundSprites.add(self.Loading)

        self.UpperSprite = PygameSprite("hitObject.png", vector2(0, 0),
                                        SkinSource.user, Positions.topCentre,
                                        Positions.centre, Color(102, 66, 245),
                                        Clocks.audio)

        self.UpperSprite.Scale(0.2)
        self.LowerSprite = PygameSprite("hitObject.png", vector2(0, 0),
                                        SkinSource.user,
                                        Positions.bottomCentre,
                                        Positions.centre, Color(245, 64, 64),
                                        Clocks.audio)
        self.LowerSprite.Scale(0.2)
        CONST.Scheduler.AddNow(self.loadElements)

    def Fail(self):
        if self.finished:
            return
        self.failed = True
        CONST.AudioManager.play(self.failSound)
        CONST.AudioManager.Pause(False)
        for sprite in CONST.foregroundSprites.sprites:
            sprite.ClearTransformations()
            sprite.FadeTo(0, 200)
        self.failQuit.enabled = True
        self.failRetry.enabled = True
        self.failOverlay.FadeTo(1, 200)
        self.failRetry.FadeTo(1, 200)
        self.failQuit.FadeTo(1, 200)

    def loadElements(self):

        if not self.isLoading:
            return

        workToDo = len(self.fileBody)
        workDone = 0

        for note in self.fileBody:
            note = note.split("|")
            if int(note[1]) == 1:
                self.upperSprites.append(
                    PygameNote(int(note[0]), NotePos.Upper, self.ar,
                               self.UpperSprite))
            else:
                self.lowerSprites.append(
                    PygameNote(int(note[0]), NotePos.Lower, self.ar,
                               self.LowerSprite))
            workDone += 1
            self.lifeBar.VectorScale(
                vector2(((workDone / workToDo) * 100) * 19.2, 5))

        lastElement = max([max(sprite.time for sprite in self.upperSprites),
                           max(sprite.time for sprite in self.lowerSprites)])

        self.ClosingTime = lastElement + self.od * 3

        self.Loading.ClearTransformations()
        self.Loading.FadeTo(0, 200)
        CONST.Scheduler.AddDelayed(200, CONST.foregroundSprites.remove,
                                   sprite=self.Loading)
        self.isLoading = False
        if ((self.upperSprites[0].time < 3000) or
                (self.lowerSprites[0].time < 3000)):
            CONST.Scheduler.AddDelayed(3000, CONST.AudioManager.Unpause,
                                       notif=False)
            NotificationMassive("Starting in 3", 1000,
                                NotificationType.Error).show()
            CONST.Scheduler.AddDelayed(1000,
                                       NotificationMassive("Starting in 2",
                                                           1000,
                                                           NotificationType.Warning).show)
            CONST.Scheduler.AddDelayed(2000,
                                       NotificationMassive("Starting in 1",
                                                           1000,
                                                           NotificationType.Info).show)
            CONST.Scheduler.AddDelayed(3000, NotificationMassive(
                "Good Luck, Have Fun", 1000, NotificationType.Info).show)
        else:
            CONST.AudioManager.Unpause()

    def updateCombo(self, hit):
        self.comboIndicatorOv.ClearTransformations()
        self.comboIndicator.ClearTransformations()
        if self.combo > self.maxCombo:
            self.maxCombo = self.combo
        fadeTime = 300

        hitColor = [Color(255, 0, 0), Color(255, 106, 0), Color(75, 235, 30),
                    Color(48, 248, 255)][hit]
        self.comboIndicator.Text(str(self.combo) + "x")
        self.comboIndicator.Color(hitColor)
        self.comboIndicator.FadeColorTo(Color(255, 255, 255), 500)

        self.comboIndicatorOv.Text(str(self.combo) + "x")
        self.comboIndicatorOv.Color(hitColor)
        self.comboIndicatorOv.FadeColorTo(Color(255, 255, 255), 500)
        self.comboIndicatorOv.Scale(1.5)
        self.comboIndicatorOv.ScaleTo(1, fadeTime, EaseTypes.easeIn)
        self.comboIndicatorOv.Fade(0.7)
        self.comboIndicatorOv.FadeTo(0, fadeTime, EaseTypes.easeIn)

    def updateScore(self):
        self.ScoreIndicator.Text(str(self.score))

    def Key1(self, holding):
        if holding and not self.key1Holt:
            self.upperOv.ClearTransformations()
            self.upperOv.Fade(1)
            CONST.AudioManager.play(self.touchSound)
            self.handleKey1()
            self.key1Holt = True
        if not holding and self.key1Holt:
            self.upperOv.FadeTo(0, 200)
            self.key1Holt = False

    def Key2(self, holding):
        if holding and not self.key2Holt:
            self.lowerOv.ClearTransformations()
            self.lowerOv.Fade(1)
            CONST.AudioManager.play(self.touchSound)
            self.handleKey2()
            self.key2Holt = True
        if not holding and self.key2Holt:
            self.lowerOv.FadeTo(0, 200)
            self.key2Holt = False

    def handleKey1(self):
        if len(self.upperSprites) > 0:
            spriteToHandle = self.upperSprites[0]
            delay = spriteToHandle.time - pygame.mixer.music.get_pos()

            if delay < 0:
                late = True
            else:
                late = False

            if abs(delay) > int(self.od) * 3:
                return
            self.unstableRate.append(delay)
            CONST.AudioManager.play(self.hitSound)
            spriteToHandle.Hit()
            self.upperSprites.pop(0)
            self.combo += 1

            if abs(delay) < int(self.od):
                self.updateCombo(3)
                self.score += 300 * self.combo
                self.accList.append(100)
                self.life += self.hp

            elif abs(delay) < int(self.od) * 2:
                self.updateCombo(2)
                self.score += 100 * self.combo
                self.accList.append(66)
                self.life += self.hp / 2

            elif abs(delay) <= int(self.od) * 3:
                self.updateCombo(1)
                self.score += 50 * self.combo
                self.accList.append(33)
                self.life += self.hp / 3

            self.updateScore()

    def handleKey2(self):
        if len(self.lowerSprites) > 0:

            spriteToHandle = self.lowerSprites[0]
            delay = spriteToHandle.time - pygame.mixer.music.get_pos()

            if delay < 0:
                late = True
            else:
                late = False

            if abs(delay) > int(self.od) * 3:
                return

            self.unstableRate.append(delay)
            CONST.AudioManager.play(self.hitSound)
            spriteToHandle.Hit()
            self.lowerSprites.pop(0)
            self.combo += 1

            if abs(delay) < int(self.od):
                self.updateCombo(3)
                self.score += 300 * self.combo
                self.accList.append(100)
                self.life += self.hp

            elif abs(delay) < int(self.od) * 2:
                self.updateCombo(2)
                self.score += 100 * self.combo
                self.accList.append(66)
                self.life += self.hp / 2

            elif abs(delay) <= int(self.od) * 3:
                self.updateCombo(1)
                self.score += 50 * self.combo
                self.accList.append(33)
                self.life += self.hp / 3

            self.updateScore()

    @property
    def isPausing(self):
        try:
            return not (self.upperSprites[
                            0].time - pygame.mixer.music.get_pos() < 3000 or
                        self.lowerSprites[
                            0].time - pygame.mixer.music.get_pos() < 3000)
        except:
            return False

    def updateLife(self):
        if not self.finished and not self.isLoading and not \
                pygame.mixer.music.get_pos() < 30 and not self.isPausing:
            self.life -= self.hp / 100
            self.life = min(self.life, 100)
            self.life = max(self.life, 0)
            self.lifeBar.VectorScale(vector2(self.life * 19.2, 5))
            if self.life == 0 and not self.failed:
                self.Fail()

    def update(self):
        currentWidth = (pygame.mixer.music.get_pos() /
                        CONST.AudioManager.currentSong["length"]) * \
                       CONST.windowManager.widthScaled

        self.progressBar.VectorScale(vector2(currentWidth, 5))
        seconds = str(int((pygame.mixer.music.get_pos() / 1000) % 60))

        if len(seconds) == 1:
            seconds = "0" + seconds

        minutes = str(int((pygame.mixer.music.get_pos() / 1000 / 60) % 60))
        self.LengthTime.Text("{}:{}".format(minutes, seconds))
        self.accBar.Fade(helper.getSyncValue(0.8, 0.5, EaseTypes.easeOut))
        self.updateLife()
        if len(self.upperSprites) > 0 and self.upperSprites[
            0].time - pygame.mixer.music.get_pos() < 0 - self.od * 3 and \
                pygame.mixer.music.get_pos() > 30:
            self.upperSprites[0].Miss()
            self.life -= self.hp
            self.upperSprites.pop(0)
            self.combo = 0
            self.updateCombo(0)
            self.accList.append(0)

        if len(self.lowerSprites) > 0 and self.lowerSprites[
            0].time - pygame.mixer.music.get_pos() < 0 - self.od * 3 and \
                pygame.mixer.music.get_pos() > 30:
            self.lowerSprites[0].Miss()
            self.life -= self.hp
            self.lowerSprites.pop(0)
            self.combo = 0
            self.updateCombo(0)
            self.accList.append(0)

        if pygame.mixer.music.get_pos() >= self.ClosingTime and \
                self.ClosingTime != 0 and not self.finished and \
                not self.isLoading:
            self.Finish()
        if self.isPausing and not self.paused:
            self.paused = True
            CONST.Background.FadeTo(0.7, 400, EaseTypes.easeInOut)
        elif not self.isPausing and self.paused:
            self.paused = False
            CONST.Background.FadeTo(0.1, 400, EaseTypes.easeInOut)

    def dispose(self):
        for sprite in CONST.foregroundSprites.sprites:
            sprite.FadeTo(0, 400)

    def HandleEvents(self, events):
        keys = pygame.key.get_pressed()
        if not self.failed and not self.finished:

            if keys[K_d] or keys[K_f]:
                self.Key1(True)
            else:
                self.Key1(False)

            if keys[K_j] or keys[K_KP4]:
                self.Key2(True)
            else:
                self.Key2(False)

        if keys[K_ESCAPE] and not self.finished:
            CONST.MenuManager.ChangeMenu(type=Menus.SongSelection)

        for event in events:
            if event.type == pygame.QUIT and not self.finished:
                CONST.MenuManager.ChangeMenu(type=Menus.SongSelection)
