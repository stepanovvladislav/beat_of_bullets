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
from scripts.main.pygameElements import PygameText

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

    def PlayMusic(self, songFolder, Preview=False):
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

    def loadSound(self, filename, skinSource):
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
            songs = os.listdir(CONST.currentDirectory + "/.user/maps")

            if len(songs) == 0:
                self.isPlaying = False
                pygame.mixer.music.set_pos(0)
            else:

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

                self.PlayMusic("/.user/maps/" + song)

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
