import os

from scripts.main.data import *
from scripts.manager.sprite import SpriteManager

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
clock = None
MenuManager = None
AudioManager = None
db = None
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
