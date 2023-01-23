import os

from scripts.main.data import *
from scripts.manager.sprite import SpriteManager

Debug = False
Running = False

Name = "BoB"
Version = "16012023"
currentSkin = "user"
windowManager = WindowManager()
cursorPos = vector2(0, 0)
UserEvents = {}
currentDirectory = os.getcwd()
surface = None
Config = None
Difficulty = None
cache = None
clock = None
MenuManager = None
AudioManager = None
enemy = None
db = None
PixelWhite = "pixel.png"
Starting = True
Background = None
Scheduler = None
Logger = None
Afk = False
LastActive = None
Framerate = 30

volume = 1

backgroundSprites = SpriteManager()
foregroundSprites = SpriteManager()
overlaySprites = SpriteManager()

WindowLeft = None
WindowCenter = None
WindowRight = None
