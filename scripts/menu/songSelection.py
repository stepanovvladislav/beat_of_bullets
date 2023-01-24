import os
import time
from os import path

import pygame
from pygame.locals import *

from scripts import CONST
from scripts.main import helper
from scripts.main.data import *
from scripts.main.pygameElements import PygameButton, PygameText, PygameSprite


class SongSelection:
    def __init__(self):
        self.Transition = False
        self.disposeTime = 400
        self.SoundHover = CONST.AudioManager.loadSound("button-hover.wav",
                                                       SkinSource.local)
        self.SoundClick = CONST.AudioManager.loadSound("button-select.wav",
                                                       SkinSource.local)
        self.SoundBack = CONST.AudioManager.loadSound("button-back.wav",
                                                      SkinSource.local)
        self.SoundChange = CONST.AudioManager.loadSound("song-change.wav",
                                                        SkinSource.local)

        self.tabBg = None
        self.tabPic = None
        self.tabPicBg = None

        self.PlayButton = None

        self.songTitle = None
        self.songArtist = None
        self.songMapper = None
        self.songBPM = None
        self.ezDefRating = None
        self.hrDefRating = None
        self.inDefRating = None
        self.offset = 0

        self.DifficultyRating = None
        self.NoteSpeed = None
        self.health = None
        self.Accuracy = None
        self.Length = None
        self.objCount = None

        self.isMouseDown = False
        self.oldMousePos = None
        self.selectorLastActive = time.time() * 1000
        self.selectorInPlace = True
        self.selectorInPlaceOffset = 0

        self.scoreScore = None
        self.scoreAcc = None
        self.scoreConsistency = None
        self.scoreCombo = None
        self.scoreRank = None
        self.scorePerf = None
        self.scoreGood = None
        self.scoreMeh = None
        self.scoreMiss = None
        self.diffName = None
        self.diffNameOverlay = None
        self.songList = []

    def general_init(self):
        if not CONST.AudioManager.isPlaying:
            CONST.AudioManager.Unpause(False)
        CONST.Framerate = 30
        background = PygameSprite(CONST.PixelWhite, vector2(0, 0),
                                  SkinSource.local,
                                  Positions.topCentre, Positions.topCentre,
                                  Color(20, 20, 20))
        background.VectorScale(vector2(CONST.windowManager.widthScaled,
                                       CONST.windowManager.heightScaled))
        background.AlphaMask("songSelectBg.png")
        CONST.foregroundSprites.add(background)

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
        button.onClick(CONST.MenuManager.ChangeMenu,
                       type=Menus.CharacterSelection)
        CONST.foregroundSprites.add(button)

        play_button = PygameButton("Start", vector2(200, 100),
                                   FontStyle.regular,
                                   vector2(
                                       CONST.windowManager.widthScaled - 200,
                                       CONST.windowManager.heightScaled - 50),
                                   Color(52, 237, 132))
        play_button.text.position = vector2(-10, 20)
        play_button.onClick(CONST.AudioManager.play, sound=self.SoundClick)
        play_button.onClick(CONST.MenuManager.ChangeMenu, type=Menus.Playing)
        CONST.foregroundSprites.add(play_button)
        self.PlayButton = play_button

        if "/data/files/intro" in CONST.AudioManager.currentSong["folder"]:
            CONST.AudioManager.Skip()
        CONST.AudioManager.ChangeBackground(
            CONST.AudioManager.currentSong["folder"] + "/background.png", 400)

        tab = PygameSprite(
            CONST.AudioManager.currentSong["folder"] + "/background.png",
            vector2(45, 0), SkinSource.absolute,
            Positions.centreLeft, Positions.centreLeft)
        tab.BottomGradiant(Color(50, 50, 50), "half")
        tab.crop(600, 800)
        tab.borderBounds(10)
        CONST.foregroundSprites.add(tab)
        self.tabBg = tab
        tab.Fade(0)
        tab.FadeTo(1, 400)
        songSelectionHeader = PygameSprite("SongSelectionHeader.png",
                                           vector2(0, 0),
                                           SkinSource.local,
                                           Positions.topCentre,
                                           Positions.topCentre,
                                           Color(50, 50, 50))

        tabPicBg = PygameSprite(CONST.PixelWhite, vector2(95, 390),
                                SkinSource.local,
                                Positions.centreLeft,
                                Positions.bottomLeft)
        tabPicBg.VectorScale(vector2(500, 500))
        tabPicBg.borderBounds(10)
        self.tabPicBg = tabPicBg
        CONST.foregroundSprites.add(tabPicBg)
        tabPic = PygameSprite(
            CONST.AudioManager.currentSong["folder"] + "/thumb.png",
            vector2(105, 380), SkinSource.absolute,
            Positions.centreLeft, Positions.bottomLeft)
        tabPic.Scale(
            480 / tabPic.image.get_width() * CONST.windowManager.getPixelSize())
        tabPic.borderBounds(10)
        CONST.foregroundSprites.add(tabPic)
        self.tabPic = tabPic

        SongTitle = PygameText(CONST.AudioManager.currentSong["name"], 45,
                               FontStyle.bold, vector2(-20, 0),
                               Positions.centreRight, Positions.centreRight)
        CONST.foregroundSprites.add(SongTitle)
        self.songTitle = SongTitle

        SongArtist = PygameText(CONST.AudioManager.currentSong["artist"], 45,
                                FontStyle.regular, vector2(-20, 30),
                                Positions.centreRight, Positions.centreRight)
        CONST.foregroundSprites.add(SongArtist)

        self.songArtist = SongArtist

        SongBpm = PygameText(
            str(CONST.AudioManager.currentSong["bpm"]) + "bpm", 45,
            FontStyle.thin, vector2(-20, 60),
            Positions.centreRight, Positions.centreRight)
        CONST.foregroundSprites.add(SongBpm)
        self.songBPM = SongBpm

        SongMapper = PygameText(
            str("Map created by " + CONST.AudioManager.currentSong["mapper"]),
            45, FontStyle.thin,
            vector2(-20, 90), Positions.centreRight, Positions.centreRight)
        CONST.foregroundSprites.add(SongMapper)
        self.songMapper = SongMapper

        diffNormal = PygameSprite(CONST.PixelWhite, vector2(300, 250),
                                SkinSource.local, Positions.centre,
                                Positions.topLeft,
                                Color(62, 194, 194))
        diffNormal.VectorScale(vector2(200, 150))
        diffNormal.onHover(CONST.AudioManager.play, sound=self.SoundHover)
        diffNormal.onHover(diffNormal.FadeTo, value=1, duration=100)
        diffNormal.onClick(self.loadDiff, difficulty=Difficulty.Normal)
        diffNormal.onHoverLost(diffNormal.FadeTo, value=0.8, duration=100)
        diffNormal.tag = "NormalDifficulty"
        diffNormal.borderBounds(20)

        diffNormal.Fade(0.8)
        CONST.foregroundSprites.add(diffNormal)

        diffHard = PygameSprite(CONST.PixelWhite, vector2(510, 250),
                                SkinSource.local, Positions.centre,
                                Positions.topLeft,
                                Color(189, 163, 60))
        diffHard.VectorScale(vector2(200, 150))
        diffHard.onHover(CONST.AudioManager.play, sound=self.SoundHover)
        diffHard.onHover(diffHard.FadeTo, value=1, duration=100)
        diffHard.onClick(self.loadDiff, difficulty=Difficulty.Hard)
        diffHard.onHoverLost(diffHard.FadeTo, value=0.8, duration=100)
        diffHard.tag = "HardDifficulty"

        diffHard.Fade(0.8)
        CONST.foregroundSprites.add(diffHard)

        diffInsane = PygameSprite(CONST.PixelWhite, vector2(720, 250),
                                  SkinSource.local, Positions.centre,
                                  Positions.topLeft,
                                  Color(147, 60, 194))
        diffInsane.VectorScale(vector2(200, 150))
        diffInsane.onHover(CONST.AudioManager.play, sound=self.SoundHover)
        diffInsane.onHover(diffInsane.FadeTo, value=1, duration=100)
        diffInsane.onClick(self.loadDiff, difficulty=Difficulty.Insane)
        diffInsane.onHoverLost(diffInsane.FadeTo, value=0.8, duration=100)
        diffInsane.tag = "InsaneDifficulty"

        diffInsane.Fade(0.8)
        CONST.foregroundSprites.add(diffInsane)

        NormalText = PygameText("Normal", 40, FontStyle.regular,
                              vector2(227, 220),
                              Positions.centre, Positions.bottomCentre)
        CONST.foregroundSprites.add(NormalText)
        NormalText.tag = "NormalDifficulty"

        NormalDiff = PygameText("-", 50, FontStyle.heavy, vector2(227, 190),
                              Positions.centre, Positions.bottomCentre)
        CONST.foregroundSprites.add(NormalDiff)
        NormalDiff.tag = "NormalDifficulty"
        self.ezDefRating = NormalDiff

        HardText = PygameText("Hard", 40, FontStyle.regular, vector2(347, 220),
                              Positions.centre, Positions.bottomCentre)
        CONST.foregroundSprites.add(HardText)
        HardText.tag = "HardDifficulty"

        HardDiff = PygameText("-", 50, FontStyle.heavy, vector2(347, 190),
                              Positions.centre, Positions.bottomCentre)
        CONST.foregroundSprites.add(HardDiff)
        HardDiff.tag = "HardDifficulty"
        self.hrDefRating = HardDiff

        InsaneText = PygameText("Insane", 40, FontStyle.regular,
                                vector2(467, 220),
                                Positions.centre, Positions.bottomCentre)
        CONST.foregroundSprites.add(InsaneText)
        InsaneText.tag = "InsaneDifficulty"

        InsaneDiff = PygameText("-", 50, FontStyle.heavy, vector2(467, 190),
                                Positions.centre, Positions.bottomCentre)
        CONST.foregroundSprites.add(InsaneDiff)
        InsaneDiff.tag = "InsaneDifficulty"
        self.inDefRating = InsaneDiff

        RankLetter = PygameSprite("/ranks/x.png", vector2(-50, -230),
                                  SkinSource.local, Positions.centre,
                                  Positions.centre)
        RankLetter.Scale(0.8)
        self.scoreRank = RankLetter
        CONST.foregroundSprites.add(RankLetter)

        value = PygameText("Score: -", 35, FontStyle.regular, vector2(-170, 0),
                           Positions.centre, Positions.centreLeft)
        self.scoreScore = value
        CONST.foregroundSprites.add(self.scoreScore)

        value = PygameText("Accuracy: -", 35, FontStyle.regular,
                           vector2(-170, 30),
                           Positions.centre, Positions.centreLeft)
        self.scoreAcc = value
        CONST.foregroundSprites.add(self.scoreAcc)

        value = PygameText("Unstable Rate: -", 35, FontStyle.regular,
                           vector2(-170, 60), Positions.centre,
                           Positions.centreLeft)
        self.scoreConsistency = value
        CONST.foregroundSprites.add(self.scoreConsistency)

        value = PygameText("Combo: -", 35, FontStyle.regular,
                           vector2(-170, 90),
                           Positions.centre, Positions.centreLeft)
        self.scoreCombo = value
        CONST.foregroundSprites.add(self.scoreCombo)

        value = PygameText("Perfect Hits: -", 35, FontStyle.regular,
                           vector2(-170, 120), Positions.centre,
                           Positions.centreLeft)
        self.scorePerf = value
        CONST.foregroundSprites.add(self.scorePerf)

        value = PygameText("Good Hits: -", 35, FontStyle.regular,
                           vector2(-170, 150), Positions.centre,
                           Positions.centreLeft)
        self.scoreGood = value
        CONST.foregroundSprites.add(self.scoreGood)

        value = PygameText("Meh Hits: -", 35, FontStyle.regular,
                           vector2(-170, 180),
                           Positions.centre, Positions.centreLeft)
        self.scoreMeh = value
        CONST.foregroundSprites.add(self.scoreMeh)

        value = PygameText("Misses: -", 35, FontStyle.regular,
                           vector2(-170, 210),
                           Positions.centre, Positions.centreLeft)
        self.scoreMiss = value
        CONST.foregroundSprites.add(self.scoreMiss)

        background.Fade(0)
        button.Fade(0)

        self.DifficultyRating = PygameText("Difficulty Rating | -", 45,
                                           FontStyle.thin, vector2(-20, -50),
                                           Positions.centreRight,
                                           Positions.centreRight)
        self.NoteSpeed = PygameText("Note Speed | -", 45, FontStyle.thin,
                                    vector2(-20, -80), Positions.centreRight,
                                    Positions.centreRight)
        self.health = PygameText("Health Drain | -", 45, FontStyle.thin,
                                 vector2(-20, -110), Positions.centreRight,
                                 Positions.centreRight)
        self.Accuracy = PygameText("Accuracy needed | -", 45, FontStyle.thin,
                                   vector2(-20, -140), Positions.centreRight,
                                   Positions.centreRight)
        self.objCount = PygameText("Object count | -", 45, FontStyle.thin,
                                   vector2(-20, -170), Positions.centreRight,
                                   Positions.centreRight)
        self.Length = PygameText("Length | -", 45, FontStyle.thin,
                                 vector2(-20, -200), Positions.centreRight,
                                 Positions.centreRight)
        self.diffName = PygameText("-", 120, FontStyle.heavy,
                                   vector2(-20, -250),
                                   Positions.centreRight,
                                   Positions.centreRight)
        self.diffNameOverlay = PygameText("-", 120, FontStyle.heavy,
                                          vector2(-20, -250),
                                          Positions.centreRight,
                                          Positions.centreRight)
        self.diffName.Fade(0.5)
        self.diffNameOverlay.Fade(0.5)
        CONST.foregroundSprites.add(self.diffName)
        CONST.foregroundSprites.add(self.diffNameOverlay)
        CONST.foregroundSprites.add(self.DifficultyRating)
        CONST.foregroundSprites.add(self.NoteSpeed)
        CONST.foregroundSprites.add(self.health)
        CONST.foregroundSprites.add(self.Accuracy)
        CONST.foregroundSprites.add(self.objCount)
        CONST.foregroundSprites.add(self.Length)

        background.FadeTo(1, 400)
        button.FadeTo(1, 400)
        CONST.foregroundSprites.add(songSelectionHeader)
        self.init()

    def init(self):
        enemy = CONST.currentDirectory + "/.user/maps/" + CONST.enemy + '/'
        songs = os.listdir(enemy)
        indexMin = 0 - 0.5 * len(songs)
        index = 0
        song = ''
        songSprite = None

        for song in songs:
            songSprite = PygameSprite(enemy + song + "/thumb.png",
                                      vector2(0, 0), SkinSource.absolute,
                                      Positions.topCentre, Positions.topCentre)
            songSprite.Scale(
                150 / songSprite.image.get_width() * CONST.windowManager.getPixelSize())
            songSprite.position = vector2((indexMin + index) * 160,
                                          -20 - abs((indexMin + index) * 10))
            songSprite.tag = "SongSelectSprite"
            if enemy + song == CONST.AudioManager.currentSong["folder"]:
                self.offset = (indexMin + index) * 160
            CONST.foregroundSprites.add(songSprite)
            self.songList.append(songSprite)
            songSprite.onHover(songSprite.VectorScaleTo,
                               scale=vector2(1.1, 1.1), duration=200,
                               easing=EaseTypes.BounceOut)
            songSprite.onHover(CONST.AudioManager.play, sound=self.SoundHover)
            songSprite.onHoverLost(songSprite.VectorScaleTo,
                                   scale=vector2(1, 1), duration=100,
                                   easing=EaseTypes.easeInOut)
            songSprite.onClick(CONST.AudioManager.play, sound=self.SoundChange)
            songSprite.onClick(self.GetNewSong, songPath=song,
                               difficulty=Difficulty.Normal, sender=songSprite)
            songSprite.data.append((indexMin + index) * 160)
            songSprite.data.append(enemy + song)
            index += 1
        self.loadDiffs()
        self.GetNewSong(song, songSprite, Difficulty.Normal)

    def GetNewSong(self, songPath, sender, difficulty=None):
        songPath = "/.user/maps/" + CONST.enemy + '/' + songPath
        if not CONST.currentDirectory + songPath == \
               CONST.AudioManager.currentSong["folder"]:
            CONST.AudioManager.Stop(False)
            CONST.AudioManager.PlayMusic(songFolder=songPath, Preview=True)
            CONST.AudioManager.ChangeBackground(
                CONST.currentDirectory + songPath + "/background.png", 100)
            self.songTitle.Text(CONST.AudioManager.currentSong["name"])
            self.songArtist.Text(CONST.AudioManager.currentSong["artist"])
            self.songBPM.Text(
                str(CONST.AudioManager.currentSong["bpm"]) + "bpm")
            self.songMapper.Text(
                "Map created by " + CONST.AudioManager.currentSong["mapper"])
            tab = PygameSprite(
                CONST.AudioManager.currentSong["folder"] + "/background.png",
                vector2(45, 0),
                SkinSource.absolute, Positions.centreLeft,
                Positions.centreLeft)
            tab.BottomGradiant(Color(50, 50, 50), "half")
            tab.crop(600, 800)
            self.tabBg.FadeTo(0, 100)
            tab.Fade(0)
            tab.FadeTo(1, 100)
            tab.borderBounds(10)
            CONST.Scheduler.AddDelayed(100, CONST.foregroundSprites.remove,
                                       sprite=self.tabBg)
            self.tabBg = tab
            CONST.foregroundSprites.add(self.tabBg)

            tabPic = PygameSprite(
                CONST.AudioManager.currentSong["folder"] + "/thumb.png",
                vector2(105, 380),
                SkinSource.absolute, Positions.centreLeft,
                Positions.bottomLeft)
            tabPic.Scale(
                480 / tabPic.image.get_width() * CONST.windowManager.getPixelSize())
            self.tabPic.FadeTo(0, 100)
            tabPic.Fade(0)
            tabPic.FadeTo(1, 100)
            tabPic.borderBounds(10)
            CONST.foregroundSprites.remove(self.tabPicBg)
            CONST.foregroundSprites.add(self.tabPicBg)
            CONST.Scheduler.AddDelayed(100, CONST.foregroundSprites.remove,
                                       sprite=self.tabPic)
            CONST.foregroundSprites.add(tabPic)
            self.tabPic = tabPic
            self.selectorInPlaceOffset = sender.data[0]
            CONST.Scheduler.AddNow(self.updateOffset, to=sender.data[0],
                                   duration=500, easing=EaseTypes.easeOut)
            self.loadDiffs()
            if difficulty is not None:
                self.loadDiff(difficulty)

    def loadDiffs(self):
        seconds = str(
            int((CONST.AudioManager.currentSong["length"] / 1000) % 60))
        if len(seconds) == 1:
            seconds = "0" + seconds
        minutes = str(
            int((CONST.AudioManager.currentSong["length"] / 1000 / 60) % 60))
        self.Length.Text("Length | {}:{}".format(minutes, seconds))
        if path.exists(
                CONST.AudioManager.currentSong["folder"] + "/normal.dd"):
            with open(CONST.AudioManager.currentSong[
                          "folder"] + "/normal.dd") as f:
                data = f.read().split("\n")
                for sprite in CONST.foregroundSprites.sprites:
                    if sprite.tag == "NormalDifficulty":
                        sprite.enable()
                self.ezDefRating.Text(data[0].split("|")[0])
                deffNormal = True
        else:
            deffNormal = False
            for sprite in CONST.foregroundSprites.sprites:
                if sprite.tag == "NormalDifficulty":
                    sprite.disable()

        if path.exists(CONST.AudioManager.currentSong["folder"] + "/hard.dd"):
            with open(
                    CONST.AudioManager.currentSong[
                        "folder"] + "/hard.dd") as f:
                data = f.read().split("\n")

                for sprite in CONST.foregroundSprites.sprites:
                    if sprite.tag == "HardDifficulty":
                        sprite.enable()
            self.hrDefRating.Text(data[0].split("|")[0])
            diffHard = True
        else:
            diffHard = False
            for sprite in CONST.foregroundSprites.sprites:
                if sprite.tag == "HardDifficulty":
                    sprite.disable()

        if path.exists(
                CONST.AudioManager.currentSong["folder"] + "/insane.dd"):
            with open(CONST.AudioManager.currentSong[
                          "folder"] + "/insane.dd") as f:
                data = f.read().split("\n")

                for sprite in CONST.foregroundSprites.sprites:
                    if sprite.tag == "InsaneDifficulty":
                        sprite.enable()
            self.inDefRating.Text(data[0].split("|")[0])
            diffInsane = True
        else:
            diffInsane = False
            for sprite in CONST.foregroundSprites.sprites:
                if sprite.tag == "InsaneDifficulty":
                    sprite.disable()
        if deffNormal:
            return self.loadDiff(Difficulty.Normal)
        elif diffHard:
            return self.loadDiff(Difficulty.Hard)
        elif diffInsane:
            return self.loadDiff(Difficulty.Insane)
        else:
            return self.loadDiff(None)

    def updateOffset(self, to, duration, easing=EaseTypes.linear):
        origin = self.offset
        now = time.time() * 1000
        while self.offset != to:
            self.offset = helper.getTimeValue(now, now + duration, origin, to,
                                              easing)

    def loadDiff(self, difficulty):
        if difficulty is None:
            self.Accuracy.Text("Accuracy Needed | -")
            self.NoteSpeed.Text("Note Speed | -")
            self.health.Text("Health Drain | -")
            self.DifficultyRating.Text("Difficulty Rating | -")
            self.diffName.Text("-")
            self.diffNameOverlay.Text("-")

            self.PlayButton.disable()

        elif difficulty == Difficulty.Normal:
            if path.exists(
                    CONST.AudioManager.currentSong["folder"] + "/normal.dd"):
                with open(CONST.AudioManager.currentSong[
                              "folder"] + "/normal.dd") as f:
                    raw = f.read().split("\n")
                    data = raw[0].split("|")
                    self.objCount.Text(
                        "Object count | {}".format(len(raw) - 1))
                    self.Accuracy.Text("Accuracy Needed | {}".format(data[1]))
                    self.NoteSpeed.Text("Note Speed | {}".format(data[2]))
                    self.health.Text("Health Drain | {}".format(data[3]))
                    self.DifficultyRating.Text(
                        "Difficulty Rating | {}".format(data[0]))
                    self.diffName.Text("Normal")
                    self.diffNameOverlay.Text("Normal")
                    CONST.Difficulty = Difficulty.Normal
                    self.PlayButton.enable()
            else:
                self.loadDiff(None)
        elif difficulty == Difficulty.Hard:
            if path.exists(
                    CONST.AudioManager.currentSong["folder"] + "/hard.dd"):
                with open(CONST.AudioManager.currentSong[
                              "folder"] + "/hard.dd") as f:
                    raw = f.read().split("\n")
                    data = raw[0].split("|")
                    self.objCount.Text(
                        "Object count | {}".format(len(raw) - 1))
                    self.Accuracy.Text("Accuracy Needed | {}".format(data[1]))
                    self.NoteSpeed.Text("Note Speed | {}".format(data[2]))
                    self.health.Text("Health Drain | {}".format(data[3]))
                    self.DifficultyRating.Text(
                        "Difficulty Rating | {}".format(data[0]))
                    self.diffName.Text("Hard")
                    self.diffNameOverlay.Text("Hard")
                    CONST.Difficulty = Difficulty.Hard
                    self.PlayButton.enable()
            else:
                self.loadDiff(None)
        elif difficulty == Difficulty.Insane:
            if path.exists(
                    CONST.AudioManager.currentSong["folder"] + "/insane.dd"):
                with open(CONST.AudioManager.currentSong[
                              "folder"] + "/insane.dd") as f:
                    raw = f.read().split("\n")
                    data = raw[0].split("|")
                    self.objCount.Text(
                        "Object count | {}".format(len(raw) - 1))
                    self.Accuracy.Text("Accuracy Needed | {}".format(data[1]))
                    self.NoteSpeed.Text("Note Speed | {}".format(data[2]))
                    self.health.Text("Health Drain | {}".format(data[3]))
                    self.DifficultyRating.Text(
                        "Difficulty Rating | {}".format(data[0]))
                    self.diffName.Text("Insane")
                    self.diffNameOverlay.Text("Insane")
                    CONST.Difficulty = Difficulty.Insane
                    self.PlayButton.enable()

            else:
                self.loadDiff(None)
        self.setScore(difficulty)

    def setScore(self, difficulty):
        if difficulty == Difficulty.Normal:
            text = "normal"
        elif difficulty == Difficulty.Hard:
            text = "hard"
        elif difficulty == Difficulty.Insane:
            text = "insane"
        else:
            text = "none"
        sqlData = CONST.db.fetch(
            "SELECT * FROM scores WHERE mapid = {} and difficulty = '{}' ORDER BY score DESC".format(
                CONST.AudioManager.currentSong["id"],
                text))
        if sqlData is None:
            self.scoreScore.Text("Score: -")
            self.scoreAcc.Text("Accuracy: -")
            self.scoreConsistency.Text("Unstable Rate: -")
            self.scoreCombo.Text("Combo: -")
            self.scorePerf.Text("Perfect Hits: -")
            self.scoreGood.Text("Good Hits: -")
            self.scoreMeh.Text("Meh Hits: -")
            self.scoreMiss.Text("Misses: -")
            RankLetter = PygameSprite("/ranks/x.png", vector2(-50, -210),
                                      SkinSource.local, Positions.centre,
                                      Positions.centre)
            RankLetter.Scale(0.8)
            RankLetter.Fade(0)
            RankLetter.FadeTo(1, 200)
            self.scoreRank.FadeTo(0, 200)
            CONST.Scheduler.AddDelayed(200, CONST.foregroundSprites.remove,
                                       sprite=self.scoreRank)
            CONST.foregroundSprites.add(RankLetter)
            self.scoreRank = RankLetter
        else:
            self.scoreScore.Text("Score: {}".format(sqlData["score"]))
            self.scoreAcc.Text("Accuracy: {}%".format(sqlData["accuracy"]))
            self.scoreConsistency.Text(
                "Unstable Rate: {}ms".format(sqlData["consistency"]))
            self.scoreCombo.Text("Combo: {}x".format(sqlData["comboMax"]))
            self.scorePerf.Text(
                "Perfect Hits: {}".format(sqlData["countPerf"]))
            self.scoreGood.Text("Good Hits: {}".format(sqlData["countGood"]))
            self.scoreMeh.Text("Meh Hits: {}".format(sqlData["countMeh"]))
            self.scoreMiss.Text("Misses: {}".format(sqlData["countMiss"]))
            RankLetter = PygameSprite("/ranks/{}.png".format(sqlData["rank"]),
                                      vector2(-50, -210), SkinSource.local,
                                      Positions.centre,
                                      Positions.centre)
            RankLetter.Scale(0.8)
            RankLetter.Fade(0)
            RankLetter.FadeTo(1, 200)
            self.scoreRank.FadeTo(0, 200)
            CONST.Scheduler.AddDelayed(200, CONST.foregroundSprites.remove,
                                       sprite=self.scoreRank)
            CONST.foregroundSprites.add(RankLetter)
            self.scoreRank = RankLetter

    def update(self):
        self.diffNameOverlay.Scale(
            helper.getSyncValue(1, 1.1, EaseTypes.easeOut))
        self.diffNameOverlay.Fade(
            helper.getSyncValue(0.5, 0, EaseTypes.easeOut))
        self.tabPicBg.Fade(helper.getSyncValue(1, 0.9, EaseTypes.easeOut))
        index = 0
        indexMin = 0 - 0.5 * len(self.songList)
        indexMax = len(self.songList) - 0.5 * len(self.songList)
        if self.isMouseDown:
            self.selectorLastActive = time.time() * 1000
            self.selectorInPlace = False
            move = self.oldMousePos.x - CONST.cursorPos.x
            if indexMax * 160 > self.offset + move > indexMin * 160:
                self.offset += move
        self.oldMousePos = CONST.cursorPos

        for sprite in self.songList:
            sprite.position = vector2(((indexMin + index) * 160) - self.offset,
                                      -20 - abs((
                                                        indexMin + index - self.offset / 160) * 10))
            index += 1

        if (
                time.time() * 1000) - self.selectorLastActive > 5000 and not self.selectorInPlace:
            self.selectorInPlace = True
            CONST.Scheduler.AddNow(self.updateOffset,
                                   to=self.selectorInPlaceOffset, duration=500,
                                   easing=EaseTypes.easeOut)

    def dispose(self):
        for sprite in CONST.foregroundSprites.sprites:
            sprite.FadeTo(0, 400)
        pass

    def HandleEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                CONST.AudioManager.play(self.SoundBack)
                CONST.MenuManager.ChangeMenu(Menus.CharacterSelection)
            if event.type == pygame.KEYDOWN:
                if not self.Transition:
                    if event.key == K_ESCAPE:
                        CONST.AudioManager.play(self.SoundBack)
                        CONST.MenuManager.ChangeMenu(Menus.CharacterSelection)
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
            if event.type == CONST.UserEvents["MUSIC_END"]:
                CONST.AudioManager.SeekPreview()
