import json
import math
import os
import random
import time
from os import path

import pygame
from mutagen.mp3 import MP3

from scripts import CONST
from scripts.main.data import *
from scripts.main.pygameElements import PygameSprite, PygameText

last = 0


class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.isPlaying = False
        self.currentSong = {}
        MUSIC_END = pygame.USEREVENT + 1
        CONST.UserEvents["MUSIC_END"] = MUSIC_END
        pygame.mixer.music.set_endevent(CONST.UserEvents["MUSIC_END"])
        self.alreadyPlayed = {}

    def BeatCount(self):
        beatLength = self.BeatLength()
        return math.ceil(self.currentSong["length"] / beatLength)

    def BeatsSinceBegin(self):
        BeatLength = self.BeatLength()
        return math.ceil(pygame.mixer.music.get_pos() / BeatLength)

    def Restart(self):
        songFolder = self.currentSong["folder"]
        pygame.mixer.music.stop()
        pygame.mixer.music.load(songFolder + "/audio.mp3")
        pygame.mixer.music.set_volume(CONST.volume)
        pygame.mixer.music.play(0)
        self.isPlaying = True

    def PlayMusic(self, songFolder: str, Preview=False):
        songFolder = CONST.currentDirectory + songFolder
        pygame.mixer.music.load(songFolder + "/audio.mp3")

        song = MP3(songFolder + "/audio.mp3")
        pygame.mixer.music.set_volume(CONST.volume)

        f = open(songFolder + "/metadata.json").read()
        self.currentSong = json.loads(f)
        self.currentSong["folder"] = songFolder
        self.currentSong["filename"] = songFolder + "/audio.mp3"
        self.currentSong["length"] = int(song.info.length * 1000)
        if not Preview:
            pygame.mixer.music.play(0)
        else:
            pygame.mixer.music.play(0, self.currentSong["previewpoint"] / 100)
        self.isPlaying = True

    def SeekPreview(self):
        pygame.mixer.music.play(start=self.currentSong["previewpoint"] / 1000)

    def loadSound(self, filename: str, skinSource: int):
        if skinSource == SkinSource.user and path.exists(
                CONST.currentDirectory + "/.user/skins/" + CONST.currentSkin + "/" + filename):
            source = CONST.currentDirectory + "/.user/skins/" + CONST.currentSkin + "/" + filename
        else:
            source = CONST.currentDirectory + "/data/sounds/" + filename
        return pygame.mixer.Sound(source)

    def play(self, sound):
        sound.set_volume(CONST.volume)
        sound.play()

    def setVolume(self, x):
        x = round(x, 2)
        CONST.volume = x
        CONST.Config.setValue("volume", x, "float")
        pygame.mixer.music.set_volume(x)

    def OnMusicEnd(self):
        global last
        if time.time() * 1000 - last < 300:
            return
        else:
            last = time.time() * 1000
        forceStop = True
        if self.isPlaying == True:
            forceStop = False
        if forceStop:
            self.isPlaying = False
        else:
            songs = os.listdir(
                CONST.currentDirectory + "/.user/maps/" + CONST.enemy + '/')

            if len(songs) == 0:
                self.isPlaying = False
                pygame.mixer.music.set_pos(0)
            else:
                song = ''
                if len(self.alreadyPlayed.values()) == len(songs):
                    FirstTime = sorted(self.alreadyPlayed.keys())[0]
                    song = self.alreadyPlayed[FirstTime]
                    self.alreadyPlayed.pop(FirstTime)
                    self.alreadyPlayed[time.time()] = song
                else:
                    found = False
                    while not found:
                        song = random.choice(songs)
                        if song not in self.alreadyPlayed.values():
                            found = True
                            self.alreadyPlayed[time.time()] = song

                self.PlayMusic("/.user/maps/" + CONST.enemy + "/" + song)

    def ChangeBackground(self, Filename, duration=500):
        if not path.exists(Filename):
            Filename = CONST.currentDirectory + "/data/sprites/background.png"
        new = PygameSprite(Filename, vector2(0, 0), SkinSource.absolute,
                           Positions.centre, Positions.centre)
        backgroundScale = CONST.windowManager.width / new.image.get_width()
        new.Scale(backgroundScale * 1.3)
        new.Fade(0)
        CONST.backgroundSprites.add(new)
        new.FadeTo(1, duration)
        CONST.Scheduler.AddDelayed(duration, CONST.backgroundSprites.remove,
                                   sprite=CONST.Background)
        CONST.Background = new

    def Stop(self, notif=True):
        self.isPlaying = False
        pygame.mixer.music.stop()

    def Pause(self, notif=True):
        self.isPlaying = False
        pygame.mixer.music.pause()

    def Unpause(self, notif=True):
        self.isPlaying = True
        pygame.mixer.music.unpause()

    def Skip(self, notif=True):
        self.isPlaying = False
        pygame.mixer.music.stop()
        self.isPlaying = True
        self.OnMusicEnd()

    def IsNewBeat(self):
        if self.currentSong == {} or not self.isPlaying:
            return False
        bpm = self.currentSong["bpm"]
        offset = self.currentSong["offset"]
        beatLength = 60000 / bpm
        if int(((pygame.mixer.music.get_pos() - offset) % beatLength)) == 0:
            return True
        else:
            return False

    def BeatLength(self):
        if self.currentSong == {} or not self.isPlaying:
            return 1000
        else:
            return 60000 / self.currentSong["bpm"]

    def GetRelativePos(self):
        if self.currentSong == {} or not self.isPlaying:
            return int(time.time() * 1000) % 1000
        bpm = self.currentSong["bpm"]
        offset = self.currentSong["offset"]
        beatLength = 60000 / bpm
        pos = pygame.mixer.music.get_pos()
        return int(((pos - offset) % beatLength)) / beatLength


class AudioMeter:
    def __init__(self):
        self.active = False
        self.lastActive = 0
        self.background = PygameSprite(CONST.PixelWhite, vector2(0, 0),
                                       SkinSource.local, Positions.centreRight,
                                       Positions.centreRight, Color(0, 0, 0))
        self.background.VectorScale(vector2(30, 600))
        self.foreground = PygameSprite(CONST.PixelWhite, vector2(-13, 290),
                                       SkinSource.local, Positions.centreRight,
                                       Positions.bottomCentre,
                                       Color(255, 204, 212))
        self.text = PygameText("100%", 20, FontStyle.regular, vector2(10, 180),
                               Positions.centreRight, Positions.centreRight)
        self.foreground.VectorScale(vector2(10, CONST.volume * 580))

    def Update(self):
        if (time.time() * 1000) - self.lastActive > 3000 and self.active:
            self.hide()
            self.active = None

    def ChangeVolume(self, up):
        if not self.active:
            self.show()
            self.active = True
        self.lastActive = time.time() * 1000
        if up:
            if CONST.volume <= 1:
                if CONST.volume < 0.10:
                    CONST.volume += 0.01
                else:
                    CONST.volume += 0.05
                if CONST.volume > 1:
                    CONST.volume = 1
                CONST.AudioManager.setVolume(CONST.volume)
        else:
            if CONST.volume >= 0:
                if CONST.volume < 0.10:
                    CONST.volume -= 0.01
                else:
                    CONST.volume -= 0.05
                if CONST.volume < 0:
                    CONST.volume = 0
                CONST.AudioManager.setVolume(CONST.volume)
        self.foreground.VectorScaleTo(vector2(10, CONST.volume * 580), 100,
                                      EaseTypes.easeOut)
        self.text.Text(str(math.floor(CONST.volume * 100)) + "%")

    def show(self):
        self.background.Fade(0)
        self.foreground.Fade(0)
        self.text.Fade(0)
        self.background.FadeTo(0.7, 200, EaseTypes.easeInOut)
        self.foreground.FadeTo(1, 200, EaseTypes.easeInOut)
        self.text.FadeTo(1, 200, EaseTypes.easeInOut)
        CONST.overlaySprites.add(self.background)
        CONST.overlaySprites.add(self.text)
        CONST.overlaySprites.add(self.foreground)

    def hide(self):
        self.background.FadeTo(0, 200, EaseTypes.easeInOut)
        self.foreground.FadeTo(0, 200, EaseTypes.easeInOut)
        self.text.FadeTo(0, 200, EaseTypes.easeInOut)
        CONST.Scheduler.AddDelayed(200, CONST.overlaySprites.remove,
                                   sprite=self.background)
        CONST.Scheduler.AddDelayed(200, CONST.overlaySprites.remove,
                                   sprite=self.text)
        CONST.Scheduler.AddDelayed(200, CONST.overlaySprites.remove,
                                   sprite=self.foreground)
