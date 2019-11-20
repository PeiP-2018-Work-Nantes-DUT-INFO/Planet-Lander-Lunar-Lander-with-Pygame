from lander import *
from random import randint
import pygame;
class Landing:
    @staticmethod
    def __init__(self):
        self.plateforms = self.getPlateformsCoords()
        self.segments = self
        return False;

    def getPlateformsCoords(self, numberOfPlateforms):
        listPlateforms = []
        for i in range(0, numberOfPlateforms):
            plateformLength = randint(LangingConfig.minSegmentOfLanding, LangingConfig.maxSegmentOfLanding) * LangingConfig.segmentPxLength
            min = (i) * Gameconfig.windowW / numberOfPlateforms
            max = min + Gameconfig.windowW / numberOfPlateforms - plateformLength
            xPos = randint(min, max)
            yPos = randint(LangingConfig.minSegmentOfLanding, LangingConfig.maxHeightPlateformLanding)
            listPlateforms.append((xPos, yPos, plateformLength))

    def draw(self, window):
        pygame.draw.lines(window, Gameconfig.white, self.plateforms())
        return False;


class LangingConfig:
    segmentPxLength = 5;
    minSegmentOfLanding = 2;
    maxSegmentOfLanding = 5;
    minHeightPlateformLanding = Gameconfig.windowH * 0.5
    maxHeightPlateformLanding = Gameconfig.windowH - 20;
