from scripts import CONST
from scripts.main.data import *
from scripts.menu.mainMenu import MainMenu
from scripts.menu.play import Gameplay
from scripts.menu.rank import RankingPanel
from scripts.menu.songSelection import SongSelection
from scripts.menu.characterSelector import CharacterSelector


class MenuManager:
    def __init__(self):
        self.activeMenu = None
        self.MenuType = None

    def ChangeMenu(self, type, enemy=None):
        """Handle menu changing, disposing the actual menu """
        if self.activeMenu != None:
            self.activeMenu.dispose()
            disposeTime = self.activeMenu.disposeTime
            for sprite in CONST.foregroundSprites.sprites:
                CONST.Scheduler.AddDelayed(disposeTime,
                                           CONST.foregroundSprites.remove,
                                           sprite=sprite)
        self.MenuType = type
        self.activeMenu = self.getMenuFromType(type)
        if type == Menus.SongSelection:
            if enemy:
                CONST.enemy = enemy
            self.activeMenu.general_init()
        else:
            self.activeMenu.init()

    def getMenuFromType(self, type):
        if type == Menus.MainMenu:
            return MainMenu()
        elif type == Menus.SongSelection:
            return SongSelection()
        elif type == Menus.Playing:
            return Gameplay()
        elif type == Menus.Ranking:
            return RankingPanel()
        elif type == Menus.CharacterSelection:
            return CharacterSelector()

    def HandleEvents(self, events):
        self.activeMenu.HandleEvents(events)
