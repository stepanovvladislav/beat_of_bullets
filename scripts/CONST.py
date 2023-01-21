import os

from scripts.main.data import *
from scripts.manager.sprite import SpriteManager

Running = False

Name = "BoB"
Version = "16012023"
currentSkin = "user"
windowManager = WindowManager()
cursorPos = vector2(0, 0)
currentDirectory = os.getcwd()
surface = None
Config = None
clock = None
db = None
PixelWhite = "pixel.png"
Framerate = 30

volume = 1

backgroundSprites = SpriteManager()
foregroundSprites = SpriteManager()
overlaySprites = SpriteManager()
