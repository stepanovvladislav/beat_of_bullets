import os
from datetime import datetime
from time import time

from scripts import CONST


class Log:
    def __init__(self):

        if not os.path.exists('logs'):
            os.makedirs('logs')
        with open("logs/runtime.log", "w") as f:
            f.write(
                ("-" * 50) + "\nRunning Beat of Bullets {}\n".format(
                    CONST.Version))
            f.write(("-" * 50) + "\n")
            if not os.path.exists('.user'):
                f.write("Creating .user folder")
                os.makedirs('.user')
                f.write("Creating .user/maps folder")
                os.makedirs('.user/maps')
                f.write("Creating .user/skins folder")
                os.makedirs('.user/skins')
                f.write("Creating .user/skins/user folder")
                os.makedirs('.user/skins/user')

    def debug(self, text):
        with open(CONST.currentDirectory + "/logs/runtime.log", "a") as f:
            f.write("\n[{}][DEBUG] : {}".format(
                datetime.utcfromtimestamp(time()).strftime('%H:%M:%S'),
                text))

    def write(self, text):
        with open(CONST.currentDirectory + "/logs/runtime.log", "a") as f:
            f.write("\n[{}][Log] : {}".format(
                datetime.utcfromtimestamp(time()).strftime('%H:%M:%S'), text))

    def error(self, text):
        with open(CONST.currentDirectory + "/logs/runtime.log", "a") as f:
            f.write("\n[{}][Error] : {}".format(
                datetime.utcfromtimestamp(time()).strftime('%H:%M:%S'), text))

    def info(self, text):
        with open(CONST.currentDirectory + "/logs/runtime.log", "a") as f:
            f.write("\n[{}][Info] : {}".format(
                datetime.utcfromtimestamp(time()).strftime('%H:%M:%S'), text))
