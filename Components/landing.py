from GameConfig import GameConfig
from random import randint, choice
import pygame
import bisect
import math


# Algorithme itératif de déplacement du point central
def midpoint_displacement(start, end, roughness, limit, vertical_displacement=None,
                          num_of_iterations=16):
    """
    Étant donné un segment de ligne droite spécifié par un point de départ et un point d'arrivée
    sous la forme de[point_de_départ_x, point_de_départ_y] et[point_de_terminaison_x, point_de_terminaison_y],
    une valeur de rugosité > 0, un déplacement vertical initial et un nombre de
    itérations > 0 applique l'algorithme du point médian au segment spécifié et
    retourne la liste de points obtenue sous la forme
    points = [[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]].

    """
    # Nombre final de points = (2^iterations)+1
    if vertical_displacement is None:
        #  si aucun déplacement initial n'est spécifié, régler le déplacement sur :
        #  (y_start+y_end)/2
        vertical_displacement = (start[1] + end[1]) / 2
    # La structure de données qui stocke les points est une liste de listes où
    #      chaque sous-liste représente un point et contient ses coordonnées x et y :
    #      points=[[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]]
    #                  |           |               |
    #              point 0      point 1         point n
    #      La liste des points est toujours triée de la plus petite à la plus grande valeur x.
    points = [start, end]
    iteration = 1
    while iteration <= num_of_iterations:
        # Comme la liste des points sera mise à jour dynamiquement avec la nouvelle valeur calculée de
        # Nombre de points après chaque déplacement du point médian, il est nécessaire de créer une copie.
        # de l'état au début de l'itération pour qu'on puisse répéter l'itération sur
        # la séquence originale.
        # Le type Tuple est utilisé pour des raisons de sécurité car ils sont immuables en Python.

        points_tup = tuple(points)
        for i in range(len(points_tup) - 1):
            # Calculez les coordonnées des points médians x et y :
            # [(x_i+x_(i+1))/2, (y_i+y_(i+1))/2]
            midpoint = list(map(lambda x: (points_tup[i][x] + points_tup[i + 1][x]) / 2,
                                [0, 1]))
            # Déplacer le point médian de la coordonnée y
            goingUpDisplacement = -vertical_displacement
            goingDownDisplacement = vertical_displacement
            if midpoint[1] + goingUpDisplacement < limit[0]:
                goingUpDisplacement = -(midpoint[1] - limit[0])
            if midpoint[1] + goingDownDisplacement > limit[1]:
                goingDownDisplacement = limit[1] - midpoint[1]
            midpoint[1] += choice([goingUpDisplacement,
                                   goingDownDisplacement])
            # Insérer le point médian déplacé dans la liste de points courante
            bisect.insort(points, midpoint)
            #  bisect permet d'insérer un élément dans une liste de façon à ce que son ordre
            #  est préservé.
            #  Par défaut, l'ordre maintenu va de la plus petite à la plus grande liste en premier.
            #  élément qui est ce que nous voulons.
        # Réduire la plage de déplacement
        vertical_displacement *= 2 ** (-roughness)
        # mise à jour du nombre d'itérations
        iteration += 1
    return points


''' class Landing 
    Usage :
        - Placement des zones d'attérissages 
        - Regroupement des fonctions de dessin de la carte    
'''


class Landing:
    def __init__(self):
        self.landingEntities = pygame.sprite.Group()
        self.plateforms = Landing.generate_plateforms(LandingConfig.numberOfPlateforms)
        self.landingStroke = LandingStroke(self.plateforms)
        self.landingEntities.add(self.landingStroke)
        for plateform in self.plateforms:
            plateformSprite = LandingPlateform(plateform)
            self.landingEntities.add(plateformSprite)

    ''' function generate_plateforms
        Usage : 
            - génère les plateformes sur lesquels le vaisseau se pose
        Arguments :
            - number_of_plateforms : nombre de plateformes qui seront placées dans la zone de jeux    
    '''

    @staticmethod
    def generate_plateforms(number_of_plateforms):
        listPlateforms = []
        for i in range(0, number_of_plateforms):
            number_of_segments = randint(LandingConfig.minSegmentOfLanding,
                                         LandingConfig.maxSegmentOfLanding)
            plateform_length = number_of_segments * LandingConfig.segmentPxLength
            min = (i) * GameConfig.windowW / number_of_plateforms
            max = min + GameConfig.windowW / number_of_plateforms - plateform_length
            xPos = randint(min + 1, max)
            yPos = randint(LandingConfig.minHeightPlateformLanding, LandingConfig.maxHeightPlateformLanding)
            percentageDifficulty = (number_of_segments - LandingConfig.minSegmentOfLanding) / (
                    LandingConfig.maxSegmentOfLanding - LandingConfig.minSegmentOfLanding)
            index = math.floor((len(LandingConfig.bonuses) - 1) * percentageDifficulty)
            bonus = LandingConfig.bonuses[index]
            listPlateforms.append((xPos, yPos, plateform_length, bonus))
        return listPlateforms


''' class Landing 
    Usage :
        - Placement des zones d'attérissages 
        - Dessin de la géographie de la planete     
'''


class LandingPlateform(pygame.sprite.DirtySprite):
    def __init__(self, plateformCoords):
        pygame.sprite.Sprite.__init__(self)
        self.dirty = 2
        self.delay = 0
        self.highLight = False
        self.coords = plateformCoords
        self.image = pygame.Surface(
            [plateformCoords[2], LandingConfig.segmentWidthPlateform + LandingConfig.fontSizeBonus], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.coords[0], self.coords[1])
        self.draw()
        self.mask = pygame.mask.from_surface(self.image, 0)

    def draw(self):
        pygame.draw.line(self.image, LandingConfig.colorPlateform, (0, 0),
                         (self.coords[2],
                          0), LandingConfig.segmentWidthPlateform)

    def update(self):
        if self.coords[3] == 0:
            return
        if self.delay > LandingConfig.delayBlinkingPlateform:
            self.image.fill((255, 255, 255, 0))
            self.draw()
            self.highLight = not self.highLight
            self.delay = 0
            self.dirty = 1
        if self.highLight:
            middle = self.coords[2] / 2
            font = pygame.font.Font(None, LandingConfig.fontSizeBonus)
            img = font.render('x' + str(self.coords[3]), True, LandingConfig.colorTextBonus)
            display_rect = img.get_rect()
            display_rect.centerx = middle
            display_rect.bottom = display_rect.height + LandingConfig.segmentWidthPlateform + \
                                  LandingConfig.offsetTextBonus
            self.image.blit(img, display_rect)
        self.delay += 1


''' class Landing 
    Usage :
        - Fais les calculs nécéssaires à la randominsation de la map
        - S'assure de la cohérence de la géographie de la map
'''


class LandingStroke(pygame.sprite.Sprite):
    def __init__(self, plateforms):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([GameConfig.windowW, LandingConfig.height], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.plateforms = plateforms
        self.segments = self.fill_segments(self.plateforms)
        self.draw_map(self.image)
        self.mask = pygame.mask.from_surface(self.image, 0)

    ''' function fill_segments 
        Usage : 
            - Donne la valeur des plateforme (multiplicateur de points)
            - Fait clignoter les plateformes et les bonus
        Arguments : 
            - self : objet courant
            - plateforms : la plateforme données en paramètre 
    '''

    def fill_segments(self, plateforms):
        segments = []
        plateforms_copy = plateforms.copy()
        plateforms_copy.insert(0, [0, GameConfig.windowH / 2, 0])
        plateforms_copy.append([GameConfig.windowW, GameConfig.windowH / 2, 0])
        for i in range(0, len(plateforms_copy) - 1):
            space_between_plateform = plateforms_copy[i + 1][0] - (plateforms_copy[i][0] + plateforms_copy[i][2])
            number_of_segments = math.ceil(
                math.log(math.ceil(space_between_plateform / LandingConfig.lengthOfSegmentsXBetweenPlateforms), 2))
            start = [plateforms_copy[i][0] + plateforms_copy[i][2], plateforms_copy[i][1]]
            end = [plateforms_copy[i + 1][0], plateforms_copy[i + 1][1]]
            vertical_displacement = self.get_best_vertical_displacement(plateforms_copy[i], start, end)
            segments.extend(midpoint_displacement(start, end, LandingConfig.roughness,
                                                  (LandingConfig.minHeightMap, LandingConfig.maxHeightMap),
                                                  vertical_displacement, num_of_iterations=number_of_segments))
            if LandingConfig.drawDebug:
                self.draw_displacement_debug(start, end, vertical_displacement, segments)

        return segments

    ''' function get_best_vertical_displacement 
        Usage : 
            - Calcul du déplcement vertical d'un point médian entre deux point déjà présent 
        Arguments : 
            - self : objet courant 
            - plateform : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            - start : début du segment 
            - end : fin du segment 
    '''

    def get_best_vertical_displacement(self, plateform, start, end):
        distance = math.fabs(start[0] - end[0])
        if distance > LandingConfig.minSizeBetweenPlateformDisplacementMode1:
            return min(self.nearest_edge_distance_y(plateform), (start[1] + end[1]) / 2)
        else:
            return math.fabs(start[1] - end[1]) / 2

    def nearest_edge_distance_y(self, plateform):
        return min(math.fabs(LandingConfig.maxHeightMap - plateform[1]),
                   math.fabs(LandingConfig.minHeightMap - plateform[1]))

    def draw_map(self, window):
        for i in range(0, len(self.segments) - 1):
            pygame.draw.line(window, GameConfig.white, self.segments[i], self.segments[i + 1])
            if LandingConfig.drawDebug:
                pygame.draw.circle(self.image, GameConfig.white, [int(self.segments[i][0]), int(self.segments[i][1])],
                                   4, 4)

    def draw_displacement_debug(self, start, end, verticalDisplacement, segments):
        font = pygame.font.Font('Bender_Light.otf', 20)
        img = font.render(str(verticalDisplacement), True, LandingConfig.colorTextBonus)
        display_rect = img.get_rect()
        middle = (start[0] + end[0]) / 2
        display_rect.centerx = middle
        display_rect.top = 0
        self.image.blit(img, display_rect)
        pygame.draw.line(self.image, GameConfig.red, (middle, 0), (middle, GameConfig.windowH))
        color = [randint(0, 255), randint(0, 255), randint(0, 255)]
        pygame.draw.circle(self.image, color, [int(start[0]), int(start[1])],
                           8, 6)
        pygame.draw.circle(self.image, color, [int(end[0]), int(end[1])],
                           8, 6)
        x_distance = segments[-1][0] - segments[-2][0]
        img = font.render(str(x_distance), True, LandingConfig.colorTextBonus)
        display_rect = img.get_rect()
        middle = segments[-1][0]
        display_rect.left = middle
        display_rect.top = 0
        self.image.blit(img, display_rect)


class LandingConfig:
    numberOfPlateforms = 5
    segmentPxLength = 15
    minSizeBetweenPlateformDisplacementMode1 = 100
    lengthOfSegmentsXBetweenPlateforms = 10
    colorPlateform = GameConfig.white
    segmentWidth = 1
    segmentWidthPlateform = 8
    minSegmentOfLanding = 2
    maxSegmentOfLanding = 6
    delayBlinkingPlateform = 30
    colorTextBonus = GameConfig.white
    offsetTextBonus = 3
    fontSizeBonus = 25
    bonuses = [
        4,
        2,
        0,
        0,
        0
    ]
    minHeightPlateformLanding = GameConfig.windowH * 0.5
    maxHeightPlateformLanding = GameConfig.windowH - segmentWidthPlateform - fontSizeBonus
    minHeightMap = 150
    maxHeightMap = GameConfig.windowH * 0.98
    height = GameConfig.windowH * 1
    roughness = 1.3
    drawDebug = False