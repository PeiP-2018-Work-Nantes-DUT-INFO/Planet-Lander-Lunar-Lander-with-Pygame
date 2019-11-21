from GameConfig import GameConfig
from random import randint, choice
import pygame
import bisect
import math


# class LandingStroke(pygame.sprite.Sprite):
#     def __init__(self, a, b):
#         pygame.sprite.Sprite.__init__(self)
#         self.pt1 = a
#         self.pt2 = b
#         self.image = pygame.Surface([LangingConfig.segmentPxLength, LangingConfig.segmentPxLength])
#         pygame.draw.line(self.image, Gameconfig.white, a[0], a[1], b[0], b[1])
#         self.rect = self.image.get_rect()
#         self.mask = pygame.mask.from_surface(self.image)

# Algorithme itératif de déplacement du point central
def midpoint_displacement(start, end, roughness, vertical_displacement=None,
                          num_of_iterations=16):
    """
    Given a straight line segment specified by a starting point and an endpoint
    in the form of [starting_point_x, starting_point_y] and [endpoint_x, endpoint_y],
    a roughness value > 0, an initial vertical displacement and a number of
    iterations > 0 applies the  midpoint algorithm to the specified segment and
    returns the obtained list of points in the form
    points = [[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]
    """
    # Final number of points = (2^iterations)+1
    if vertical_displacement is None:
        # if no initial displacement is specified set displacement to:
        #  (y_start+y_end)/2
        vertical_displacement = (start[1] + end[1]) / 2
    # Data structure that stores the points is a list of lists where
    # each sublist represents a point and holds its x and y coordinates:
    # points=[[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]
    #              |          |              |
    #           point 0    point 1        point n
    # The points list is always kept sorted from smallest to biggest x-value
    points = [start, end]
    iteration = 1
    while iteration <= num_of_iterations:
        # Since the list of points will be dynamically updated with the new computed
        # points after each midpoint displacement it is necessary to create a copy
        # of the state at the beginning of the iteration so we can iterate over
        # the original sequence.
        # Tuple type is used for security reasons since they are immutable in Python.
        points_tup = tuple(points)
        for i in range(len(points_tup) - 1):
            # Calculate x and y midpoint coordinates:
            # [(x_i+x_(i+1))/2, (y_i+y_(i+1))/2]
            midpoint = list(map(lambda x: (points_tup[i][x] + points_tup[i + 1][x]) / 2,
                                [0, 1]))
            # Displace midpoint y-coordinate
            midpoint[1] += choice([-vertical_displacement,
                                   vertical_displacement])
            # Insert the displaced midpoint in the current list of points
            bisect.insort(points, midpoint)
            # bisect allows to insert an element in a list so that its order
            # is preserved.
            # By default the maintained order is from smallest to biggest list first
            # element which is what we want.
        # Reduce displacement range
        vertical_displacement *= 2 ** (-roughness)
        # update number of iterations
        iteration += 1
    return points


class Landing:
    def __init__(self):
        self.landingEntities = pygame.sprite.Group()
        self.landingStroke = LandingStroke()
        self.landingEntities.add(self.landingStroke)


class LandingStroke(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.plateforms = self.getPlateformsCoords(LangingConfig.numberOfPlateforms)
        self.image = pygame.Surface([GameConfig.windowW, LangingConfig.height])
        self.segments = self.fillSegments(self.plateforms)
        self.drawMap(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def getPlateformsCoords(self, numberOfPlateforms):
        listPlateforms = []
        for i in range(0, numberOfPlateforms):
            plateformLength = randint(LangingConfig.minSegmentOfLanding,
                                      LangingConfig.maxSegmentOfLanding) * LangingConfig.segmentPxLength
            min = (i) * GameConfig.windowW / numberOfPlateforms
            max = min + GameConfig.windowW / numberOfPlateforms - plateformLength
            xPos = randint(min, max)
            yPos = randint(LangingConfig.minHeightPlateformLanding, LangingConfig.maxHeightPlateformLanding)
            listPlateforms.append((xPos, yPos, plateformLength))
        return listPlateforms

    def fillSegments(self, plateforms):
        segments = []
        plateformsCopy = plateforms.copy()
        plateformsCopy.insert(0, [0, GameConfig.windowH / 2, 0])
        plateformsCopy.append([GameConfig.windowW, GameConfig.windowH / 2])
        for i in range(0, len(plateformsCopy) - 1):
            numberOfSegments = 16
            segments.extend(midpoint_displacement([plateformsCopy[i][0] + plateformsCopy[i][2], plateformsCopy[i][1]],
                                                  [plateformsCopy[i + 1][0], plateformsCopy[i + 1][1]],
                                                  LangingConfig.roughness, num_of_iterations=numberOfSegments))

        return segments

    def drawMap(self, window):
        for plateform in self.plateforms:
            pygame.draw.line(window, GameConfig.red, (plateform[0], plateform[1]),
                             (plateform[0] + plateform[2],
                              plateform[1]))
        it = iter(self.segments)
        for pt in it:
            nextPoint = next(it)
            pygame.draw.line(window, GameConfig.white, pt, nextPoint)



class LangingConfig:
    numberOfPlateforms = 3
    segmentPxLength = 30
    segmentWidth = 1
    minSegmentOfLanding = 1
    maxSegmentOfLanding = 3
    minHeightPlateformLanding = GameConfig.windowH * 0.5
    maxHeightPlateformLanding = GameConfig.windowH - 20
    height = GameConfig.windowH * 1
    roughness = 1.1
