import time
from os import path

import pygame

from scripts import CONST
from scripts.main import helper
from scripts.main.data import *

originMult = 1
posMult = 1


class PygameNote:
    def __init__(self, time, position, Approach, refObject):

        self.time = time
        if position == NotePos.Upper:
            color = Color(102, 66, 245)
            Field = Positions.topCentre
            mult = 1
        else:
            mult = -1
            color = Color(245, 64, 64)
            Field = Positions.bottomCentre

        self.Sprite = PygameSprite("file.png",
                                   vector2(0, 200 * mult), SkinSource.user,
                                   Field,
                                   Positions.centre, color, Clocks.audio,
                                   False)
        self.Sprite.scale = 0.2
        self.Sprite.loadFrom(refObject)
        self.Sprite.position = vector2(5550, 5550)

        if position == NotePos.Lower:
            self.Sprite.tag = "LowerElement"
        else:
            self.Sprite.tag = "UpperElement"

        CONST.foregroundSprites.add(self.Sprite)
        self.Sprite.transformations["position"]["beginTime"] = time - Approach
        self.Sprite.transformations["position"]["endTime"] = time + Approach
        self.Sprite.transformations["position"]["beginValue"] = vector2(1000,
                                                                        0)
        self.Sprite.transformations["position"]["endValue"] = vector2(-1000, 0)
        self.Sprite.transformations["position"]["easing"] = EaseTypes.linear
        self.Sprite.transformations["position"]["loop"] = False

    def Miss(self):
        self.Sprite.Color(Color(255, 0, 0))
        self.Sprite.FadeTo(0, 200)
        CONST.Scheduler.AddDelayed(200, CONST.foregroundSprites.remove,
                                   sprite=self.Sprite)

    def Hit(self):
        self.Sprite.ClearTransformations()
        self.Sprite.ScaleTo(0.3, 300, EaseTypes.easeOut)
        self.Sprite.FadeTo(0, 300, EaseTypes.easeOut)
        CONST.Scheduler.AddDelayed(300, CONST.foregroundSprites.remove,
                                   sprite=self.Sprite)


class PygameText:

    def __init__(self, text, textSize, style=FontStyle.regular,
                 position=vector2(0, 0), field=Positions.topLeft,
                 origin=Positions.topLeft, color=Color(255, 255, 255, 255),
                 clock=Clocks.game):
        global originMult
        originMult = 1 / (CONST.windowManager.getPixelSize())

        mult = int(textSize * 2.66)

        self.font = pygame.font.Font(
            CONST.currentDirectory + "/data/fonts/Torus-" + style, mult)
        self.text = self.font.render(text, True,
                                     (color.r, color.g, color.b, color.a))
        self.text = self.text.convert_alpha()
        self.field = field
        self.origin = origin
        self.Clock = clock
        self.originPosition = position
        self.posMult = posMult
        self.posMultY = posMult
        self.position = vector2(0, 0)
        self.scale = 1
        self.tag = ""
        self.transformations = {"scale": {}, "fade": {}, "VectorScale": {},
                                "position": {}, "colorFade": {},
                                "rotation": {}}
        self.alpha = 1
        self.vectorScale = vector2(1, 1)
        self.originColor = color
        self.color = color
        self.rotation = 0
        self.textSize = textSize * CONST.windowManager.getPixelSize() * 3 * 1.3
        self.offset = vector2(0, 0)
        self.effectivePosition = vector2(0, 0)
        self.onhover = []
        self.onhoverlost = []
        self.onClick = []
        self.isonHover = False
        self.enabled = True

        width = self.text.get_width()
        height = self.text.get_height()
        self.srcText = self.text.convert_alpha()
        self.unBlendedImg = self.text.convert_alpha()
        colorR = self.color.r
        colorG = self.color.g
        colorB = self.color.b
        colorA = self.color.a
        self.srcText.fill((colorR, colorG, colorB, colorA),
                          special_flags=pygame.BLEND_RGBA_MULT)

        self.text = pygame.transform.scale(self.srcText, (
            int(width * CONST.windowManager.getPixelSize() * (self.scale) / 3),
            int(height * CONST.windowManager.getPixelSize() * (
                self.scale) / 3)))
        self.UpdateStats()

    def __onHover__(self):
        for hoverAction in self.onhover:
            if hoverAction[1] == {}:
                hoverAction[0]()
            else:
                hoverAction[0](hoverAction[1])

    def __onHoverLost__(self):
        for hoverLostAction in self.onhoverlost:
            if hoverLostAction[1] == {}:
                hoverLostAction[0]()
            else:
                hoverLostAction[0](hoverLostAction[1])

    def __onClick__(self):
        for click in self.onClick:
            click[0](click[1])

    def disable(self):
        """
        Disable any transition and every input if enabled
        """
        self.enabled = False
        self.text.set_alpha(int((self.alpha / 4) * 255))
        self.HiddenColor(
            Color(self.color.r * 0.3, self.color.g * 0.3, self.color.b * 0.3))

    def enable(self):
        """
        Enable any transition and every input if disabled
        """
        self.enabled = True
        self.text.set_alpha(self.alpha)
        self.HiddenColor(self.color)

    def HiddenColor(self, color):
        """
        Same as Color, but will not register color in variable, so can be cancelled with obj.Color(obj.color)
        :param color: Color of the sprite
        """
        self.srcText = self.unBlendedImg.convert_alpha()
        self.srcText.fill((color.r, color.g, color.b, color.a),
                          special_flags=pygame.BLEND_RGBA_MULT)
        self.Scale(self.scale)

    def onHover(self, function, **kwargs):
        self.onhover.append([function, kwargs])

    def onHoverLost(self, function, **kwargs):
        self.onhoverlost.append([function, kwargs])

    def onClick(self, function, **kwargs):
        self.onClick.append([function, kwargs])

    def Rotate(self, deg, fromScale=False):
        self.rotation = deg
        self.text = pygame.transform.rotate(self.text, deg)
        self.UpdateStats()

    def Text(self, text):
        self.unBlendedImg = self.font.render(text, True, (
            self.color.r, self.color.g, self.color.b, self.color.a))
        self.srcText = self.font.render(text, True, (
            self.color.r, self.color.g, self.color.b, self.color.a))
        self.text = self.font.render(text, True, (
            self.color.r, self.color.g, self.color.b, self.color.a))
        self.UpdateStats()
        self.Scale(self.scale)
        self.Fade(self.alpha)

    def Scale(self, x):
        if CONST.windowManager.getPixelSize() > 1:
            sx = (1 / CONST.windowManager.getPixelSize()) / 2.2
        else:
            sx = (CONST.windowManager.getPixelSize()) / 2.2
        self.scale = x
        width = self.srcText.get_width()
        height = self.srcText.get_height()
        self.text = pygame.transform.scale(self.srcText, (
            int(width * CONST.windowManager.getPixelSize() * sx * x * self.vectorScale.x),
            int(height * CONST.windowManager.getPixelSize() * sx * x * self.vectorScale.y)))
        self.UpdateStats()

    def Color(self, color):
        self.srcText = self.unBlendedImg.convert_alpha()
        self.color = color
        self.srcText.fill((color.r, color.g, color.b, color.a),
                          special_flags=pygame.BLEND_RGBA_MULT)
        self.Scale(self.scale)

    def VectorScale(self, vectorScale):
        self.vectorScale = vectorScale
        self.Scale(self.scale)

    def Fade(self, x):
        self.alpha = x
        self.text.set_alpha(255 * x)

    def MoveTo(self, x, y, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["position"]["beginTime"] = time.time() * 1000
        self.transformations["position"][
            "endTime"] = time.time() * 1000 + duration
        self.transformations["position"]["beginValue"] = self.position
        self.transformations["position"]["endValue"] = vector2(x, y)
        self.transformations["position"]["easing"] = easing
        self.transformations["position"]["loop"] = loop

    def FadeTo(self, value, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["fade"]["beginTime"] = time.time() * 1000
        self.transformations["fade"]["endTime"] = time.time() * 1000 + duration
        self.transformations["fade"]["beginValue"] = self.alpha
        self.transformations["fade"]["endValue"] = value
        self.transformations["fade"]["easing"] = easing
        self.transformations["fade"]["loop"] = loop

    def FadeColorTo(self, color, duration, easing=EaseTypes.linear,
                    loop=False):
        self.transformations["colorFade"]["beginTime"] = time.time() * 1000
        self.transformations["colorFade"][
            "endTime"] = time.time() * 1000 + duration
        self.transformations["colorFade"]["beginValue"] = self.color
        self.transformations["colorFade"]["endValue"] = color
        self.transformations["colorFade"]["easing"] = easing
        self.transformations["colorFade"]["loop"] = loop

    def VectorScaleTo(self, scale, duration, easing=EaseTypes.linear,
                      loop=False):
        self.transformations["VectorScale"]["beginTime"] = time.time() * 1000
        self.transformations["VectorScale"][
            "endTime"] = time.time() * 1000 + duration
        self.transformations["VectorScale"]["beginValue"] = self.vectorScale
        self.transformations["VectorScale"]["endValue"] = scale
        self.transformations["VectorScale"]["easing"] = easing
        self.transformations["VectorScale"]["loop"] = loop

    def ScaleTo(self, scale, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["scale"]["beginTime"] = time.time() * 1000
        self.transformations["scale"][
            "endTime"] = time.time() * 1000 + duration
        self.transformations["scale"]["beginValue"] = self.scale
        self.transformations["scale"]["endValue"] = scale
        self.transformations["scale"]["easing"] = easing
        self.transformations["scale"]["loop"] = loop

    def ClearTransformations(self, type=None):
        self.transformations = {"scale": {}, "fade": {}, "VectorScale": {},
                                "position": {}, "colorFade": {},
                                "rotation": {}}

    def UpdateStats(self):
        if self.field == Positions.topLeft:
            self.offset = vector2(0, 0)
        elif self.field == Positions.topCentre:
            self.offset = vector2(CONST.windowManager.width / 2, 0)
        elif self.field == Positions.topRight:
            self.offset = vector2(CONST.windowManager.width, 0)
            self.posMult = -posMult
        elif self.field == Positions.centreLeft:
            self.offset = vector2(0, CONST.windowManager.height / 2)
        elif self.field == Positions.centre:
            self.offset = vector2(CONST.windowManager.width / 2,
                                  CONST.windowManager.height / 2)
        elif self.field == Positions.centreRight:
            self.offset = vector2(CONST.windowManager.width,
                                  CONST.windowManager.height / 2)
            self.posMult = -posMult
        elif self.field == Positions.bottomLeft:
            self.offset = vector2(0, CONST.windowManager.height)
            self.posMultY = -posMult
        elif self.field == Positions.bottomCentre:
            self.offset = vector2(CONST.windowManager.width / 2,
                                  CONST.windowManager.height)
            self.posMultY = -posMult
        elif self.field == Positions.bottomRight:
            self.offset = vector2(CONST.windowManager.width,
                                  CONST.windowManager.height)
            self.posMultY = -posMult
            self.posMult = -posMult
        width = self.text.get_width()
        height = self.text.get_height()
        if self.origin == Positions.topCentre:
            self.offset.x -= width / 2
        elif self.origin == Positions.topRight:
            self.offset.x -= width
        elif self.origin == Positions.centreLeft:
            self.offset.y -= height / 2
        elif self.origin == Positions.centre:
            self.offset.x -= width / 2
            self.offset.y -= height / 2
        elif self.origin == Positions.centreRight:
            self.offset.x -= width
            self.offset.y -= height / 2
        elif self.origin == Positions.bottomLeft:
            self.offset.y -= height
        elif self.origin == Positions.bottomCentre:
            self.offset.x -= width / 2
            self.offset.y -= height
        elif self.origin == Positions.bottomRight:
            self.offset.x -= width
            self.offset.y -= height
        self.effectivePosition = vector2(self.originPosition.x + self.offset.x,
                                         self.originPosition.y + self.offset.y)

    def draw(self):
        if self.enabled:
            if self.text.get_rect().collidepoint(
                    pygame.mouse.get_pos()) and not self.isonHover:
                self.isonHover = True
                self.__onHover__()
            elif not self.text.get_rect().collidepoint(
                    pygame.mouse.get_pos()) and self.isonHover:
                self.isonHover = False
                self.__onHoverLost__()
            if self.Clock == Clocks.game:
                now = time.time() * 1000
            else:
                now = pygame.mixer.music.get_pos()

            if self.transformations["rotation"] != {}:
                beginTime = self.transformations["rotation"]["beginTime"]
                endtime = self.transformations["rotation"]["endTime"]
                beginValue = self.transformations["rotation"]["beginValue"]
                endValue = self.transformations["rotation"]["endValue"]
                easing = self.transformations["rotation"]["easing"]
                if self.scale == endValue:
                    if self.transformations["rotation"]["loop"]:
                        duration = self.transformations["rotation"][
                                       "endTime"] - \
                                   self.transformations["rotation"][
                                       "beginTime"]
                        self.transformations["rotation"]["beginTime"] = now
                        self.transformations["rotation"][
                            "endTime"] = now + duration
                        self.transformations["rotation"][
                            "beginValue"] = endValue
                        self.transformations["rotation"][
                            "endValue"] = beginValue
                    else:
                        self.transformations["rotation"] = {}
                elif now > beginTime:
                    self.Scale(self.scale)
                    if self.Clock == Clocks.game:
                        self.Rotate(
                            helper.getTimeValue(beginTime, endtime, beginValue,
                                                endValue, easing))
                    else:
                        self.Rotate(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValue, endValue,
                                                     easing))

            if self.transformations["scale"] != {}:
                beginTime = self.transformations["scale"]["beginTime"]
                endtime = self.transformations["scale"]["endTime"]
                beginValue = self.transformations["scale"]["beginValue"]
                endValue = self.transformations["scale"]["endValue"]
                easing = self.transformations["scale"]["easing"]
                if self.scale == endValue:
                    if self.transformations["scale"]["loop"]:
                        duration = self.transformations["scale"]["endTime"] - \
                                   self.transformations["scale"][
                                       "beginTime"]
                        self.transformations["scale"]["beginTime"] = now
                        self.transformations["scale"][
                            "endTime"] = now + duration
                        self.transformations["scale"]["beginValue"] = endValue
                        self.transformations["scale"]["endValue"] = beginValue
                    else:
                        self.transformations["scale"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Scale(
                            helper.getTimeValue(beginTime, endtime, beginValue,
                                                endValue, easing))
                    else:
                        self.Scale(helper.getAudioTimeValue(beginTime, endtime,
                                                            beginValue,
                                                            endValue, easing))

            if self.transformations["fade"] != {}:
                beginTime = self.transformations["fade"]["beginTime"]
                endtime = self.transformations["fade"]["endTime"]
                beginValue = self.transformations["fade"]["beginValue"]
                endValue = self.transformations["fade"]["endValue"]
                easing = self.transformations["fade"]["easing"]
                if self.alpha == endValue:
                    if self.transformations["fade"]["loop"]:
                        duration = self.transformations["fade"]["endTime"] - \
                                   self.transformations["fade"][
                                       "beginTime"]
                        self.transformations["fade"]["beginTime"] = now
                        self.transformations["fade"][
                            "endTime"] = now + duration
                        self.transformations["fade"]["beginValue"] = endValue
                        self.transformations["fade"]["endValue"] = beginValue
                    else:
                        self.transformations["fade"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Fade(
                            helper.getTimeValue(beginTime, endtime, beginValue,
                                                endValue, easing))
                    else:
                        self.Fade(helper.getAudioTimeValue(beginTime, endtime,
                                                           beginValue,
                                                           endValue, easing))
            if self.transformations["VectorScale"] != {}:
                beginTime = self.transformations["VectorScale"]["beginTime"]
                endtime = self.transformations["VectorScale"]["endTime"]
                beginValueX = self.transformations["VectorScale"][
                    "beginValue"].x
                endValueX = self.transformations["VectorScale"]["endValue"].x
                beginValueY = self.transformations["VectorScale"][
                    "beginValue"].y
                endValueY = self.transformations["VectorScale"]["endValue"].y
                easing = self.transformations["VectorScale"]["easing"]
                if self.vectorScale.x == endValueX and self.vectorScale.y == endValueY:
                    if self.transformations["VectorScale"]["loop"]:
                        duration = self.transformations["VectorScale"][
                                       "endTime"] - \
                                   self.transformations["VectorScale"][
                                       "beginTime"]
                        self.transformations["VectorScale"]["beginTime"] = now
                        self.transformations["VectorScale"][
                            "endTime"] = now + duration
                        self.transformations["VectorScale"][
                            "beginValue"] = vector2(endValueX, endValueY)
                        self.transformations["VectorScale"][
                            "endValue"] = vector2(beginValueX, beginValueY)
                    else:
                        self.transformations["VectorScale"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.VectorScale(
                            vector2(helper.getTimeValue(beginTime, endtime,
                                                        beginValueX, endValueX,
                                                        easing),
                                    helper.getTimeValue(beginTime, endtime,
                                                        beginValueY, endValueY,
                                                        easing)))
                    else:
                        self.VectorScale(
                            vector2(
                                helper.getAudioTimeValue(beginTime, endtime,
                                                         beginValueX,
                                                         endValueX, easing),
                                helper.getAudioTimeValue(beginTime, endtime,
                                                         beginValueY,
                                                         endValueY, easing)))

            if self.transformations["colorFade"] != {}:
                beginTime = self.transformations["colorFade"]["beginTime"]
                endtime = self.transformations["colorFade"]["endTime"]

                beginValueR = self.transformations["colorFade"]["beginValue"].r
                endValueR = self.transformations["colorFade"]["endValue"].r

                beginValueG = self.transformations["colorFade"]["beginValue"].g
                endValueG = self.transformations["colorFade"]["endValue"].g

                beginValueB = self.transformations["colorFade"]["beginValue"].b
                endValueB = self.transformations["colorFade"]["endValue"].b

                easing = self.transformations["colorFade"]["easing"]
                if self.color.r == endValueR and self.color.g == endValueG and self.color.b == endValueB:
                    if self.transformations["colorFade"]["loop"]:
                        duration = self.transformations["colorFade"][
                                       "endTime"] - \
                                   self.transformations["colorFade"][
                                       "beginTime"]
                        self.transformations["colorFade"]["beginTime"] = now
                        self.transformations["colorFade"][
                            "endTime"] = now + duration
                        self.transformations["colorFade"][
                            "beginValue"] = Color(endValueR, endValueG,
                                                  endValueB)
                        self.transformations["colorFade"]["endValue"] = Color(
                            beginValueR, beginValueG, beginValueB)
                    else:
                        self.transformations["colorFade"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Color(Color(
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueR, endValueR,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueG, endValueG,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueB, endValueB,
                                                easing)))
                    else:
                        self.Color(Color(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueR, endValueR,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueG, endValueG,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueB, endValueB,
                                                     easing)))

            if self.transformations["position"] != {}:
                beginTime = self.transformations["position"]["beginTime"]
                endtime = self.transformations["position"]["endTime"]
                beginValueX = self.transformations["position"]["beginValue"].x
                endValueX = self.transformations["position"]["endValue"].x
                beginValueY = self.transformations["position"]["beginValue"].y
                endValueY = self.transformations["position"]["endValue"].y
                easing = self.transformations["position"]["easing"]
                if self.position.x == endValueX and self.position.y == endValueY:
                    if self.transformations["position"]["loop"]:
                        duration = self.transformations["position"][
                                       "endTime"] - \
                                   self.transformations["position"][
                                       "beginTime"]
                        self.transformations["position"]["beginTime"] = now
                        self.transformations["position"][
                            "endTime"] = now + duration
                        self.transformations["position"][
                            "beginValue"] = vector2(endValueX, endValueY)
                        self.transformations["position"]["endValue"] = vector2(
                            beginValueX, beginValueY)
                    else:
                        self.transformations["position"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.position = vector2(
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueX, endValueX,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueY, endValueY,
                                                easing))
                    else:
                        self.position = vector2(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueX, endValueX,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueY, endValueY,
                                                     easing))
        self.UpdateStats()
        if self.alpha != 0:
            CONST.surface.blit(self.text,
                               (
                                   self.effectivePosition.x + CONST.windowManager.getPixelSize() *
                                   int(((
                                                self.originPosition.x + self.position.x * originMult) * self.posMult) * (
                                               CONST.windowManager.getPixelSize() / 1.3)),
                                   self.effectivePosition.y + CONST.windowManager.getPixelSize() *
                                   int(((
                                                self.originPosition.y + self.position.y * originMult) * self.posMultY)) * (
                                           CONST.windowManager.getPixelSize() / 1.3)))


class PygameSprite:

    def __init__(self, filename, position, skinSource, field, origin,
                 color=Color(255, 255, 255, 255), clock=Clocks.game,
                 load=True):
        if load:
            if skinSource == SkinSource.user and path.exists(
                    CONST.currentDirectory + "/.user/skins/" +
                    CONST.currentSkin + "/" + filename):
                self.image = pygame.image.load(
                    CONST.currentDirectory + "/.user/skins/" +
                    CONST.currentSkin + "/" + filename)
            elif skinSource == SkinSource.absolute:
                self.image = pygame.image.load(filename)
            else:
                self.image = pygame.image.load(
                    CONST.currentDirectory + "/data/sprites/" + filename)
            self.image = self.image.convert_alpha()
        else:
            self.image = None
        self.filename = filename
        self.field = field
        self.Clock = clock
        self.origin = origin
        self.originPosition = position
        self.posMult = 1
        self.posMultY = 1
        self.position = vector2(0, 0)
        self.scale = 1
        self.tag = ""
        self.transformations = {"scale": {}, "fade": {}, "VectorScale": {},
                                "position": {}, "colorFade": {},
                                "rotation": {}}
        self.alpha = 1
        self.vectorScale = vector2(1, 1)
        self.originColor = color
        self.color = color
        self.rotation = 0
        self.offset = None

        self.isonHover = False
        self.onhover = []
        self.onhoverlost = []
        self.onclick = []
        self.enabled = True
        self.data = []

        if load:
            width = self.image.get_width()
            height = self.image.get_height()
            self.srcImg = self.image.convert_alpha()
            self.unBlendedImg = self.image.convert_alpha()
            colorR, colorG, colorB = self.color.r, self.color.g, self.color.b
            colorA = self.color.a
            self.srcImg.fill((colorR, colorG, colorB, colorA),
                             special_flags=pygame.BLEND_RGBA_MULT)
            self.image = pygame.transform.scale(self.srcImg, (
                int(width * CONST.windowManager.getPixelSize() * self.scale),
                int(height * CONST.windowManager.getPixelSize() * self.scale)))
            self.UpdateStats()
        else:
            self.srcImg = None
            self.unBlendedImg = None

    def loadFrom(self, other):
        self.srcImg = other.srcImg
        self.unBlendedImg = other.unBlendedImg
        self.image = other.image
        self.UpdateStats()

    def Horiflip(self):
        self.srcImg = pygame.transform.flip(self.srcImg, False, True)
        self.Scale(self.scale)

    def Vertflip(self):
        self.srcImg = pygame.transform.flip(self.srcImg, True, False)
        self.Scale(self.scale)

    def changeImageFromString(self, string, size):
        self.unBlendedImg = pygame.image.fromstring(string, size,
                                                    "RGBA").convert_alpha()
        self.Color(self.color)

    def __onHover__(self):
        for hoverAction in self.onhover:
            if hoverAction[1] == {}:
                hoverAction[0]()
            else:
                hoverAction[0](**hoverAction[1])

    def __onHoverLost__(self):
        for hoverLostAction in self.onhoverlost:
            if hoverLostAction[1] == {}:
                hoverLostAction[0]()
            else:
                hoverLostAction[0](**hoverLostAction[1])

    def __onClick__(self):
        for onClick in self.onclick:
            if onClick[1] == {}:
                onClick[0]()
            else:
                onClick[0](**onClick[1])

    def onHover(self, function, **kwargs):
        self.onhover.append([function, kwargs])

    def disable(self):
        self.enabled = False
        self.image.set_alpha(int((self.alpha / 4) * 255))
        self.HiddenColor(
            Color(self.color.r * 0.3, self.color.g * 0.3, self.color.b * 0.3))

    def enable(self):
        self.enabled = True
        self.image.set_alpha(self.alpha)
        self.HiddenColor(self.color)

    def onHoverLost(self, function, **kwargs):
        self.onhoverlost.append([function, kwargs])

    def onClick(self, function, **kwargs):
        self.onclick.append([function, kwargs])

    def Rotate(self, deg):
        self.rotation = deg
        self.image = pygame.transform.rotate(self.image, deg)
        self.UpdateStats(True)

    def borderBounds(self, borderRadius):
        self.image = pygame.image.fromstring(
            helper.cornerBounds(self, borderRadius), self.image.get_size(),
            "RGBA").convert_alpha()

    def crop(self, x, y):
        size = CONST.windowManager.getPixelSize()
        offset = vector2(0, 0)
        width = self.unBlendedImg.get_width()
        height = self.unBlendedImg.get_height()
        self.Scale(1920 / width)
        self.image = self.image.subsurface((width / 2, height / 2 - (y / 2),
                                            x * size,
                                            y * size))
        self.UpdateStats()

    def Scale(self, x):
        size = CONST.windowManager.getPixelSize()
        self.scale = x
        width = self.srcImg.get_width()
        height = self.srcImg.get_height()
        self.image = pygame.transform.scale(self.srcImg, (
            int(width * size * x * self.vectorScale.x),
            int(height * size * x * self.vectorScale.y)))
        self.image.set_alpha(255 * self.alpha)
        self.UpdateStats()

    def Color(self, color):
        self.srcImg = self.unBlendedImg.convert_alpha()
        self.color = color
        self.srcImg.fill((color.r, color.g, color.b, color.a),
                         special_flags=pygame.BLEND_RGBA_MULT)
        self.Scale(self.scale)

    def HiddenColor(self, color):
        self.srcImg = self.unBlendedImg.convert_alpha()
        self.srcImg.fill((color.r, color.g, color.b, color.a),
                         special_flags=pygame.BLEND_RGBA_MULT)
        self.Scale(self.scale)

    def FillColor(self, Color):
        self.Color(self.color)
        s = pygame.Surface((self.srcImg.get_width(), self.srcImg.get_height()))
        s.set_alpha(Color.a)
        s.fill((Color.r, Color.g, Color.b))
        self.srcImg.blit(s, (0, 0))
        self.Scale(self.scale)

    def AlphaMask(self, mask):
        mask = CONST.currentDirectory + "/data/sprites/masks/" + mask
        mask = pygame.image.load(mask)
        mask = pygame.transform.scale(mask, (
            int(self.image.get_width()), int(self.image.get_height())))
        self.image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def TopGradiant(self, color, style):
        src = "/data/sprites/gradiants/gradiant-"
        try:

            gradiant = pygame.image.load(
                CONST.currentDirectory + src + style + ".png").convert_alpha()
        except:
            gradiant = pygame.image.load(
                CONST.currentDirectory + src + "full.png").convert_alpha()

        gradiant = pygame.transform.scale(gradiant, (
            self.srcImg.get_height(), self.srcImg.get_width()))
        gradiant.fill((color.r, color.g, color.b, color.a),
                      special_flags=pygame.BLEND_RGBA_MULT)
        gradiant = pygame.transform.rotate(gradiant, -90)
        self.Color(self.color)
        self.srcImg.blit(gradiant, (0, 0))
        self.Scale(self.scale)

    def BottomGradiant(self, color, style):
        src = "/data/sprites/gradiants/gradiant-"
        try:
            gradiant = pygame.image.load(
                CONST.currentDirectory + src + style + ".png").convert_alpha()
        except:
            gradiant = pygame.image.load(
                CONST.currentDirectory + src + "full.png").convert_alpha()

        gradiant = pygame.transform.scale(gradiant, (
            self.srcImg.get_height(), self.srcImg.get_width()))
        gradiant.fill((color.r, color.g, color.b, color.a),
                      special_flags=pygame.BLEND_RGBA_MULT)
        gradiant = pygame.transform.rotate(gradiant, 90)
        self.Color(self.color)
        self.srcImg.blit(gradiant, (0, 0))
        self.Scale(self.scale)

    def VectorScale(self, vectorScale):
        self.vectorScale = vectorScale
        self.Scale(self.scale)

    def Fade(self, x):
        self.alpha = x
        self.image.set_alpha(255 * x)

    def MoveTo(self, x, y, duration, easing=EaseTypes.linear, loop=False):
        if self.Clock == Clocks.game:
            self.transformations["fade"]["beginTime"] = time.time() * 1000
        else:
            self.transformations["fade"][
                "beginTime"] = pygame.mixer.music.get_pos()
        if self.Clock == Clocks.game:
            self.transformations["fade"][
                "endTime"] = time.time() * 1000 + duration
        else:
            self.transformations["fade"][
                "endTime"] = pygame.mixer.music.get_pos() + duration
        self.transformations["position"]["beginValue"] = self.position
        self.transformations["position"]["endValue"] = vector2(x, y)
        self.transformations["position"]["easing"] = easing
        self.transformations["position"]["loop"] = loop

    def FadeTo(self, value, duration, easing=EaseTypes.linear, loop=False):
        if self.Clock == Clocks.game:
            self.transformations["fade"]["beginTime"] = time.time() * 1000
        else:
            self.transformations["fade"][
                "beginTime"] = pygame.mixer.music.get_pos()
        if self.Clock == Clocks.game:
            self.transformations["fade"][
                "endTime"] = time.time() * 1000 + duration
        else:
            self.transformations["fade"][
                "endTime"] = pygame.mixer.music.get_pos() + duration
        self.transformations["fade"]["beginValue"] = self.alpha
        self.transformations["fade"]["endValue"] = value
        self.transformations["fade"]["easing"] = easing
        self.transformations["fade"]["loop"] = loop

    def FadeColorTo(self, color, duration, easing=EaseTypes.linear,
                    loop=False):
        if self.Clock == Clocks.game:
            self.transformations["colorFade"]["beginTime"] = time.time() * 1000
        else:
            self.transformations["colorFade"][
                "beginTime"] = pygame.mixer.music.get_pos()
        if self.Clock == Clocks.game:
            self.transformations["colorFade"][
                "endTime"] = time.time() * 1000 + duration
        else:
            self.transformations["colorFade"][
                "endTime"] = pygame.mixer.music.get_pos() + duration
        self.transformations["colorFade"]["beginValue"] = self.color
        self.transformations["colorFade"]["endValue"] = color
        self.transformations["colorFade"]["easing"] = easing
        self.transformations["colorFade"]["loop"] = loop

    def VectorScaleTo(self, scale, duration, easing=EaseTypes.linear,
                      loop=False):
        if self.Clock == Clocks.game:
            self.transformations["VectorScale"][
                "beginTime"] = time.time() * 1000
        else:
            self.transformations["VectorScale"][
                "beginTime"] = pygame.mixer.music.get_pos()
        if self.Clock == Clocks.game:
            self.transformations["VectorScale"][
                "endTime"] = time.time() * 1000 + duration
        else:
            self.transformations["VectorScale"][
                "endTime"] = pygame.mixer.music.get_pos() + duration
        self.transformations["VectorScale"]["beginValue"] = self.vectorScale
        self.transformations["VectorScale"]["endValue"] = scale
        self.transformations["VectorScale"]["easing"] = easing
        self.transformations["VectorScale"]["loop"] = loop

    def ScaleTo(self, scale, duration, easing=EaseTypes.linear, loop=False):
        if self.Clock == Clocks.game:
            self.transformations["scale"]["beginTime"] = time.time() * 1000
        else:
            self.transformations["scale"][
                "beginTime"] = pygame.mixer.music.get_pos()
        if self.Clock == Clocks.game:
            self.transformations["scale"][
                "endTime"] = time.time() * 1000 + duration
        else:
            self.transformations["scale"][
                "endTime"] = pygame.mixer.music.get_pos() + duration
        self.transformations["scale"]["beginValue"] = self.scale
        self.transformations["scale"]["endValue"] = scale
        self.transformations["scale"]["easing"] = easing
        self.transformations["scale"]["loop"] = loop

    def ClearTransformations(self, type=None):
        self.transformations = {"scale": {}, "fade": {}, "VectorScale": {},
                                "position": {}, "colorFade": {},
                                "rotation": {}}

    def UpdateStats(self, init=False):
        if self.field == Positions.topLeft:
            self.offset = vector2(0, 0)
        elif self.field == Positions.topCentre:
            self.offset = vector2(CONST.windowManager.width / 2, 0)
        elif self.field == Positions.topRight:
            self.offset = vector2(CONST.windowManager.width, 0)
            if init:
                self.posMult = -1
        elif self.field == Positions.centreLeft:
            self.offset = vector2(0, CONST.windowManager.height / 2)
        elif self.field == Positions.centre:
            self.offset = vector2(CONST.windowManager.width / 2,
                                  CONST.windowManager.height / 2)
        elif self.field == Positions.centreRight:
            self.offset = vector2(CONST.windowManager.width,
                                  CONST.windowManager.height / 2)
            if init:
                self.posMult = -1
        elif self.field == Positions.bottomLeft:
            self.offset = vector2(0, CONST.windowManager.height)
            self.posMultY = -1
        elif self.field == Positions.bottomCentre:
            self.offset = vector2(CONST.windowManager.width / 2,
                                  CONST.windowManager.height)
            if init:
                self.posMultY = -1
        elif self.field == Positions.bottomRight:
            self.offset = vector2(CONST.windowManager.width,
                                  CONST.windowManager.height)
            if init:
                self.posMultY = -1
                self.posMult = -1
        width = self.image.get_width()
        height = self.image.get_height()
        if self.origin == Positions.topCentre:
            self.offset.x -= width / 2
        elif self.origin == Positions.topRight:
            self.offset.x -= width
        elif self.origin == Positions.centreLeft:
            self.offset.y -= height / 2
        elif self.origin == Positions.centre:
            self.offset.x -= width / 2
            self.offset.y -= height / 2
        elif self.origin == Positions.centreRight:
            self.offset.x -= width
            self.offset.y -= height / 2
        elif self.origin == Positions.bottomLeft:
            self.offset.y -= height
        elif self.origin == Positions.bottomCentre:
            self.offset.x -= width / 2
            self.offset.y -= height
        elif self.origin == Positions.bottomRight:
            self.offset.x -= width
            self.offset.y -= height
        self.effectivePosition = vector2(self.offset.x, self.offset.y)

    def draw(self):
        ep = self.effectivePosition
        op = self.originPosition
        if self.enabled:
            beginRect = vector2((
                    ep.x + CONST.windowManager.getPixelSize() *
                    ((op.x + self.position.x) * self.posMult)),
                ep.y + CONST.windowManager.getPixelSize() *
                ((op.y + self.position.y) * self.posMultY))
            endRect = vector2(
                beginRect.x + (self.image.get_width()),
                beginRect.y + (self.image.get_height())
            )
            actuallyHover = (((CONST.cursorPos.x > beginRect.x) and
                              (CONST.cursorPos.x < endRect.x)) and (
                                     (CONST.cursorPos.y > beginRect.y)
                                     and (CONST.cursorPos.y < endRect.y))
                             and self.alpha > 0)
            if actuallyHover and not self.isonHover:
                self.isonHover = True
                self.__onHover__()
            elif not actuallyHover and self.isonHover:
                self.isonHover = False
                self.__onHoverLost__()

            if self.Clock == Clocks.game:
                now = time.time() * 1000
            else:
                now = pygame.mixer.music.get_pos()

            if self.transformations["rotation"] != {}:
                beginTime = self.transformations["rotation"]["beginTime"]
                endtime = self.transformations["rotation"]["endTime"]
                beginValue = self.transformations["rotation"]["beginValue"]
                endValue = self.transformations["rotation"]["endValue"]
                easing = self.transformations["rotation"]["easing"]
                if self.scale == endValue:
                    if self.transformations["rotation"]["loop"]:
                        duration = self.transformations["rotation"][
                                       "endTime"] - \
                                   self.transformations["rotation"][
                                       "beginTime"]
                        self.transformations["rotation"]["beginTime"] = now
                        self.transformations["rotation"][
                            "endTime"] = now + duration
                        self.transformations["rotation"][
                            "beginValue"] = endValue
                        self.transformations["rotation"][
                            "endValue"] = beginValue
                    else:
                        self.transformations["rotation"] = {}
                elif now > beginTime:
                    self.Scale(self.scale)
                    if self.Clock == Clocks.game:
                        self.Rotate(
                            helper.getTimeValue(beginTime, endtime, beginValue,
                                                endValue, easing))
                    else:
                        self.Rotate(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValue, endValue,
                                                     easing))

            if self.transformations["scale"] != {}:
                beginTime = self.transformations["scale"]["beginTime"]
                endtime = self.transformations["scale"]["endTime"]
                beginValue = self.transformations["scale"]["beginValue"]
                endValue = self.transformations["scale"]["endValue"]
                easing = self.transformations["scale"]["easing"]
                if self.scale == endValue:
                    if self.transformations["scale"]["loop"]:
                        duration = self.transformations["scale"]["endTime"] - \
                                   self.transformations["scale"][
                                       "beginTime"]
                        self.transformations["scale"]["beginTime"] = now
                        self.transformations["scale"][
                            "endTime"] = now + duration
                        self.transformations["scale"]["beginValue"] = endValue
                        self.transformations["scale"]["endValue"] = beginValue
                    else:
                        self.transformations["scale"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Scale(
                            helper.getTimeValue(beginTime, endtime, beginValue,
                                                endValue, easing))
                    else:
                        self.Scale(helper.getAudioTimeValue(beginTime, endtime,
                                                            beginValue,
                                                            endValue, easing))

            if self.transformations["fade"] != {}:
                beginTime = self.transformations["fade"]["beginTime"]
                endtime = self.transformations["fade"]["endTime"]
                beginValue = self.transformations["fade"]["beginValue"]
                endValue = self.transformations["fade"]["endValue"]
                easing = self.transformations["fade"]["easing"]
                if self.alpha == endValue:
                    if self.transformations["fade"]["loop"]:
                        duration = self.transformations["fade"]["endTime"] - \
                                   self.transformations["fade"]["beginTime"]
                        self.transformations["fade"]["beginTime"] = now
                        self.transformations["fade"][
                            "endTime"] = now + duration
                        self.transformations["fade"]["beginValue"] = endValue
                        self.transformations["fade"]["endValue"] = beginValue
                    else:
                        self.transformations["fade"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Fade(
                            helper.getTimeValue(beginTime, endtime, beginValue,
                                                endValue, easing))
                    else:
                        self.Fade(helper.getAudioTimeValue(beginTime, endtime,
                                                           beginValue,
                                                           endValue, easing))
            if self.transformations["VectorScale"] != {}:
                beginTime = self.transformations["VectorScale"]["beginTime"]
                endtime = self.transformations["VectorScale"]["endTime"]
                beginValueX = self.transformations["VectorScale"][
                    "beginValue"].x
                endValueX = self.transformations["VectorScale"]["endValue"].x
                beginValueY = self.transformations["VectorScale"][
                    "beginValue"].y
                endValueY = self.transformations["VectorScale"]["endValue"].y
                easing = self.transformations["VectorScale"]["easing"]
                if ((self.vectorScale.x == endValueX) and
                        (self.vectorScale.y == endValueY)):
                    if self.transformations["VectorScale"]["loop"]:
                        duration = self.transformations["VectorScale"][
                                       "endTime"] - \
                                   self.transformations["VectorScale"][
                                       "beginTime"]
                        self.transformations["VectorScale"]["beginTime"] = now
                        self.transformations["VectorScale"][
                            "endTime"] = now + duration
                        self.transformations["VectorScale"][
                            "beginValue"] = vector2(endValueX, endValueY)
                        self.transformations["VectorScale"][
                            "endValue"] = vector2(beginValueX, beginValueY)
                    else:
                        self.transformations["VectorScale"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.VectorScale(vector2(
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueX, endValueX,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueY, endValueY,
                                                easing)))
                    else:
                        self.VectorScale(vector2(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueX, endValueX,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueY, endValueY,
                                                     easing)))

            if self.transformations["colorFade"] != {}:
                beginTime = self.transformations["colorFade"]["beginTime"]
                endtime = self.transformations["colorFade"]["endTime"]

                beginValueR = self.transformations["colorFade"]["beginValue"].r
                endValueR = self.transformations["colorFade"]["endValue"].r

                beginValueG = self.transformations["colorFade"]["beginValue"].g
                endValueG = self.transformations["colorFade"]["endValue"].g

                beginValueB = self.transformations["colorFade"]["beginValue"].b
                endValueB = self.transformations["colorFade"]["endValue"].b

                easing = self.transformations["colorFade"]["easing"]
                if ((self.color.r == endValueR) and
                        (self.color.g == endValueG) and
                        (self.color.b == endValueB)):
                    if self.transformations["colorFade"]["loop"]:
                        duration = self.transformations["colorFade"][
                                       "endTime"] - \
                                   self.transformations["colorFade"][
                                       "beginTime"]
                        self.transformations["colorFade"]["beginTime"] = now
                        self.transformations["colorFade"][
                            "endTime"] = now + duration
                        self.transformations["colorFade"][
                            "beginValue"] = Color(endValueR, endValueG,
                                                  endValueB)
                        self.transformations["colorFade"]["endValue"] = Color(
                            beginValueR, beginValueG, beginValueB)
                    else:
                        self.transformations["colorFade"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Color(Color(
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueR, endValueR,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueG, endValueG,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueB, endValueB,
                                                easing)))
                    else:
                        self.Color(Color(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueR, endValueR,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueG, endValueG,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueB, endValueB,
                                                     easing)))

            if self.transformations["position"] != {}:
                beginTime = self.transformations["position"]["beginTime"]
                endtime = self.transformations["position"]["endTime"]
                beginValueX = self.transformations["position"]["beginValue"].x
                endValueX = self.transformations["position"]["endValue"].x
                beginValueY = self.transformations["position"]["beginValue"].y
                endValueY = self.transformations["position"]["endValue"].y
                easing = self.transformations["position"]["easing"]
                if ((self.position.x == endValueX) and
                        (self.position.y == endValueY)):
                    if self.transformations["position"]["loop"]:
                        duration = self.transformations["position"][
                                       "endTime"] - \
                                   self.transformations["position"][
                                       "beginTime"]
                        self.transformations["position"]["beginTime"] = now
                        self.transformations["position"][
                            "endTime"] = now + duration
                        self.transformations["position"][
                            "beginValue"] = vector2(endValueX, endValueY)
                        self.transformations["position"]["endValue"] = vector2(
                            beginValueX, beginValueY)
                    else:
                        self.transformations["position"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.position = vector2(
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueX, endValueX,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueY, endValueY,
                                                easing))
                    else:
                        self.position = vector2(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueX, endValueX,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueY, endValueY,
                                                     easing))
        self.UpdateStats()
        if self.alpha != 0:
            CONST.surface.blit(self.image,
                               (ep.x + CONST.windowManager.getPixelSize() *
                                ((op.x + self.position.x) * self.posMult),
                                ep.y + CONST.windowManager.getPixelSize() *
                                ((op.y + self.position.y) * self.posMultY)))
