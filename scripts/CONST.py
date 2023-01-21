import os

from scripts.manager.sprite import SpriteManager

Running = False

Name = "BoB"
Version = "16012023"
currentDirectory = os.getcwd()
surface = None
Config = None
clock = None
db = None
Framerate = 30

volume = 1

backgroundSprites = SpriteManager()
foregroundSprites = SpriteManager()
overlaySprites = SpriteManager()
