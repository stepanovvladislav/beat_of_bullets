import time

import pygame
from PIL import Image, ImageDraw
from easing_functions import *

from scripts import CONST
from scripts.main.data import *


def getAudioTimeValue(beginTime, finalTime, beginValue, endValue,
                      easing=EaseTypes.linear):
    if pygame.mixer.music.get_busy():
        now = pygame.mixer.music.get_pos()
    else:
        now = finalTime
    timeSinceBegin = now - beginTime
    duration = finalTime - beginTime

    if timeSinceBegin < 0:
        return beginValue
    if timeSinceBegin > duration:
        return endValue
    advancement = timeSinceBegin / duration
    difference = endValue - beginValue
    return round(getEase(easing, beginValue, endValue, duration, advancement,
                         difference), 4)


def getTimeValue(beginTime, finalTime, beginValue, endValue,
                 easing=EaseTypes.linear):
    now = time.time() * 1000
    timeSinceBegin = now - beginTime
    duration = finalTime - beginTime

    if timeSinceBegin < 0:
        return beginValue
    if timeSinceBegin > duration:
        return endValue
    advancement = timeSinceBegin / duration
    difference = endValue - beginValue
    return round(getEase(easing, beginValue, endValue, duration, advancement,
                         difference), 4)


def getEase(type, begin, end, duration, advancement, difference):
    if type == EaseTypes.linear:
        return begin + advancement * difference
    if type == EaseTypes.easeIn:
        return begin + (QuadEaseIn(start=0, end=1, duration=100).ease(
            advancement * 100) * difference)
    if type == EaseTypes.easeOut:
        return begin + (QuadEaseOut(start=0, end=1, duration=100).ease(
            advancement * 100) * difference)
    if type == EaseTypes.easeInOut:
        return begin + (QuadEaseInOut(start=0, end=1, duration=100).ease(
            advancement * 100) * difference)
    if type == EaseTypes.BounceIn:
        return begin + (BounceEaseIn(start=0, end=1, duration=100).ease(
            advancement * 100) * difference)
    if type == EaseTypes.BounceOut:
        return begin + (BounceEaseOut(start=0, end=1, duration=100).ease(
            advancement * 100) * difference)
    if type == EaseTypes.BounceEaseOut:
        return begin + (BounceEaseInOut(start=0, end=1, duration=100).ease(
            advancement * 100) * difference)


def InstantQuit():
    CONST.Running = False


def cornerBounds(sprite, rad):
    im = pygame.image.tostring(sprite.image, "RGBA")
    im = Image.frombytes("RGBA",
                         (sprite.image.get_width(), sprite.image.get_height()),
                         im, "raw")

    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im.tobytes()
