import pygame
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


def getParralax(x, y):
    screenX = CONST.windowManager.width
    screenY = CONST.windowManager.height
    return x - screenX / 2, y - screenY / 2


def SetParalax(intensity):
    parraX, parraY = getParralax(CONST.cursorPos.x, CONST.cursorPos.y)
    return vector2(parraX / intensity / CONST.windowManager.getPixelSize(),
                   parraY / intensity / CONST.windowManager.getPixelSize())


def getTimeValue(beginTime, finalTime, beginValue, endValue,
                 easing=EaseTypes.linear):
    from time import time
    now = time() * 1000
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


def getSyncValue(beginValue, endValue, easing=EaseTypes.linear):
    advancement = CONST.AudioManager.GetRelativePos()
    difference = endValue - beginValue
    final = round(
        getEase(easing, beginValue, endValue, CONST.AudioManager.BeatLength(),
                advancement, difference), 4)
    if final < 0:
        return beginValue
    return final


isQuitting = False


def GameQuit():
    global isQuitting
    from pygameElements import PygameText
    if isQuitting:
        InstantQuit()
        return
    isQuitting = True
    try:
        CONST.WindowLeft.dispose()
        CONST.WindowCenter.dispose()
        CONST.WindowRight.dispose()
    except:
        pass
    CONST.AudioManager.play(
        CONST.AudioManager.loadSound("goodbye.mp3", SkinSource.user))
    CONST.AudioManager.Stop()
    CONST.MenuManager.activeMenu.Transition = True
    for sprite in CONST.foregroundSprites.sprites:
        sprite.FadeTo(0, 1000, EaseTypes.easeInOut)
    for sprite in CONST.backgroundSprites.sprites:
        sprite.FadeTo(0, 5000, EaseTypes.easeInOut)
    for sprite in CONST.overlaySprites.sprites:
        sprite.FadeTo(0, 200, EaseTypes.easeInOut)
    goodbye = PygameText("Goodbye", 70, FontStyle.regular, vector2(0, 0),
                         Positions.centre, Positions.centre)
    CONST.overlaySprites.add(goodbye)
    goodbye.FadeTo(0, 6000, EaseTypes.easeIn)
    CONST.Scheduler.AddDelayed(6000, InstantQuit)


def InstantQuit():
    CONST.Running = False


def cornerBounds(sprite, rad):
    from PIL import Image, ImageDraw
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
