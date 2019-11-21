from lander import *
from random import randint
import pygame;
from math import sqrt;


# class LandingStroke(pygame.sprite.Sprite):
#     def __init__(self, a, b):
#         pygame.sprite.Sprite.__init__(self)
#         self.pt1 = a
#         self.pt2 = b
#         self.image = pygame.Surface([LangingConfig.segmentPxLength, LangingConfig.segmentPxLength])
#         pygame.draw.line(self.image, Gameconfig.white, a[0], a[1], b[0], b[1])
#         self.rect = self.image.get_rect()
#         self.mask = pygame.mask.from_surface(self.image)


class LandingStroke(pygame.sprite.Sprite):
    @staticmethod
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.landingEntities = pygame.sprite.Group()
        self.plateforms = self.getPlateformsCoords()
        self.image = pygame.Surface([Gameconfig.windowW, LangingConfig.height])
        self.segments = []
        self.draw(self.image)

    def getPlateformsCoords(self, numberOfPlateforms):
        listPlateforms = []
        for i in range(0, numberOfPlateforms):
            plateformLength = randint(LangingConfig.minSegmentOfLanding,
                                      LangingConfig.maxSegmentOfLanding) * LangingConfig.segmentPxLength
            min = (i) * Gameconfig.windowW / numberOfPlateforms
            max = min + Gameconfig.windowW / numberOfPlateforms - plateformLength
            xPos = randint(min, max)
            yPos = randint(LangingConfig.minSegmentOfLanding, LangingConfig.maxHeightPlateformLanding)
            listPlateforms.append((xPos, yPos, plateformLength))

    def draw(self, window):
        for plateform in self.plateforms:
            pygame.draw.lines(window, Gameconfig.white, plateform[0], plateform[1], plateform[0]*plateform[1], plateform[1])

class LangingConfig:
    segmentPxLength = 5
    segmentWidth = 1
    minSegmentOfLanding = 2
    maxSegmentOfLanding = 5
    minHeightPlateformLanding = Gameconfig.windowH * 0.5
    maxHeightPlateformLanding = Gameconfig.windowH - 20
    height = Gameconfig.windowH * 0.6
