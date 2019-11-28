import pygame
from os import path


class Artificial_intelligence():
    def __init__(self, landing, aircraft):
        value_max = 0
        for plateform in landing.plateforms:
            if plateform[3] > value_max:
                self.plateform_arrivee = plateform
                value_max = plateform[3]
        if plateform[3] == 1:
            self.file = open(path.join('ressources', 'distance_1.txt'), 'r')
        elif plateform[3] == 2:
            self.file = open(path.join('ressources', 'distance_2.txt'), 'r')
        else:
            self.file = open(path.join('ressources', 'distance_4.txt'), 'r')
        self.distance = float(self.file.read())

        self.aircraft = aircraft
        self.position = "gauche"

    def get_next_commande(self):
        print(self.aircraft.orientation)
        self.aircraft.orientation %= 360
        if self.aircraft.x < (self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2) - self.distance): # On est à gauche de la plateforme
            self.position = "gauche"
            if self.aircraft.vx > 50:
                if self.aircraft.orientation != 270:
                    return self.turn_270()
                if self.aircraft.y > 140 and self.aircraft.vy > -10:
                    return pygame.K_UP
            if self.aircraft.vx < 50:
                if self.aircraft.orientation != 0:
                    return self.turn_0()
                return pygame.K_UP

        if self.aircraft.x > (self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2) + self.distance): # On est à droite de la plateforme
            self.position = "droite"
            if self.aircraft.vx > -50:
                if self.aircraft.orientation != 180:
                    return self.turn_180()
                return pygame.K_UP
            if self.aircraft.vx < -50:
                if self.aircraft.orientation != 270:
                    return self.turn_270()
                if self.aircraft.y > 140 and self.aircraft.vy > -10:
                    return pygame.K_UP
            if self.aircraft.vx < 25:
                if self.aircraft.orientation != 180.0:

                    return self.turn_180()
                return pygame.K_UP

        if (self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2) - self.distance) < self.aircraft.x < (self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2)):
            self.position = "gauche"
            if self.aircraft.vx > 0.0:
                if self.aircraft.orientation != 180:
                    return self.turn_180()
                if self.aircraft.vx > 0:
                    return pygame.K_UP

            if self.aircraft.orientation != 270:
                return self.turn_270()
            if self.aircraft.vy > 15:
                return pygame.K_UP

        if (self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2)) < self.aircraft.x < (self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2) + self.distance):
            self.position = "droite"
            if self.aircraft.vx < 0.0:
                if self.aircraft.orientation != 0:
                    return self.turn_0()
                if self.aircraft.vx < 0:
                    return pygame.K_UP

            if self.aircraft.orientation != 270:
                return self.turn_270()
            if self.aircraft.vy > 15:
                return pygame.K_UP

    def turn_0(self):
        if self.aircraft.orientation > 180.0:
            return pygame.K_RIGHT
        else:
            return pygame.K_LEFT

    def turn_270(self):
        if 90.0 < self.aircraft.orientation < 270.0:
            return pygame.K_RIGHT
        else:
            return pygame.K_LEFT

    def turn_180(self):
        if self.aircraft.orientation > 180.0:
            return pygame.K_LEFT
        else:
            return pygame.K_RIGHT

    def update_distance(self):
        if self.position == "gauche":
            if self.aircraft.x > self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2):
                self.distance *= 0.5
                self.file.write(str(self.distance))
            if self.aircraft.x < self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2):
                self.distance *= 1.5
                self.file.write(str(self.distance))
        elif self.position == "droite":
            if self.aircraft.x < self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2):
                self.distance *= 0.5
                self.file.write(str(self.distance))
            if self.aircraft.x > self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2):
                self.distance *= 1.5
                self.file.write(str(self.distance))