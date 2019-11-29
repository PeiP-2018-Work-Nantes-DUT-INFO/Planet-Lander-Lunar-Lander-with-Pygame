import pygame
from os import path


class Artificial_intelligence():
    def __init__(self, landing, aircraft):
        value_max = 0
        self.orientation_aircraft = 0
        for plateform in landing.plateforms:
            if plateform[3] > value_max:
                self.plateform_arrivee = plateform
                value_max = plateform[3]
        if self.plateform_arrivee[3] == 1:
            self.file = open(path.join('ressources', 'distance_1.txt'), 'r')
        elif self.plateform_arrivee[3] == 2:
            self.file = open(path.join('ressources', 'distance_2.txt'), 'r')
        else:
            self.file = open(path.join('ressources', 'distance_4.txt'), 'r')
        self.distance = float(self.file.read())
        self.file.close()

        self.aircraft = aircraft
        self.deceleration = False

    def get_next_command(self):
        self.orientation_aircraft = self.aircraft.orientation % 360
        print(self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2) - self.distance)
        print(self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2) + self.distance)
        print(self.aircraft.vx)
        print(self.aircraft.x)
        print('\n')
        if self.plateform_arrivee[0] < 200:
            # la condition marche pas, je sais pas pourquoi, je verrai demain matin
            if (self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2) - self.distance) > self.aircraft.x > (self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2) + self.distance):
                print('uesh')
                if self.aircraft.vx < 0:
                    return self.exception_in_the_middle()
            if self.aircraft.x < 200:
                return self.exception_from_the_left()
            if self.aircraft.x > 200:
                return self.exception_fron_the_right()

        else:
            if self.aircraft.x < (self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2) - self.distance): # On est à gauche de la plateforme
                return self.on_the_left()

            if self.aircraft.x > (self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2) + self.distance): # On est à droite de la plateforme
                return self.on_the_right()

            if (self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2) - self.distance) < self.aircraft.x < (self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2) + self.distance):
                return self.in_the_middle()


    def turn_0(self):
        if self.orientation_aircraft > 180.0:
            return pygame.K_RIGHT
        else:
            return pygame.K_LEFT

    def turn_270(self):
        if 90.0 < self.orientation_aircraft < 270.0:
            return pygame.K_RIGHT
        else:
            return pygame.K_LEFT

    def turn_180(self):
        if self.orientation_aircraft > 180.0:
            return pygame.K_LEFT
        else:
            return pygame.K_RIGHT

    def update_distance(self):
        if self.plateform_arrivee[3] == 1:
            self.file = open(path.join('ressources', 'distance_1.txt'), 'w')
        elif self.plateform_arrivee[3] == 2:
            self.file = open(path.join('ressources', 'distance_2.txt'), 'w')
        else:
            self.file = open(path.join('ressources', 'distance_4.txt'), 'w')

        if self.aircraft.x > self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2):
            print("trop loin, on miltiplie la distance par 2")
            self.distance = self.distance * 1.5
            self.file.write(str(self.distance))

        if self.aircraft.x < self.plateform_arrivee[0] + (self.plateform_arrivee[2] / 2):
            print("trop proche, on divise la distance par 2")
            self.distance = self.distance * 0.5
            self.file.write(str(self.distance))

        # print(self.distance)
        # print(self.plateform_arrivee[3])

        self.file.close()

    def on_the_left(self):
        if self.deceleration:
            return self.in_the_middle()
        elif self.aircraft.y > 100 and self.aircraft.vy > -10:
            if self.orientation_aircraft != 270:
                return self.turn_270()
            return pygame.K_UP

    def on_the_right(self):
        if self.deceleration:
            return self.in_the_middle()

    def in_the_middle(self):
        self.deceleration = True
        if self.aircraft.vx > 0.0:
            if self.orientation_aircraft != 180:
                return self.turn_180()
            if self.aircraft.vx > 0:
                return pygame.K_UP

        if self.orientation_aircraft != 270:
            return self.turn_270()
        if self.aircraft.vy > 19:
            return pygame.K_UP

    def exception_from_the_left(self):
        if self.deceleration:
            return self.exception_in_the_middle()
        elif self.aircraft.y > 100 and self.aircraft.vy > -10:
            if self.orientation_aircraft != 270:
                return self.turn_270()
            return pygame.K_UP

    def exception_fron_the_right(self):
        if self.deceleration:
            return self.exception_in_the_middle()
        elif self.aircraft.y > 100 and self.aircraft.vy > -10:
            if self.orientation_aircraft != 270:
                return self.turn_270()
            return pygame.K_UP
        elif self.aircraft.vx > -25:
            if self.orientation_aircraft != 180.0:
                return self.turn_180()
            return pygame.K_UP

    def exception_in_the_middle(self):
        print('cc')
        self.deceleration = True
        if self.aircraft.vx < 0.0:
            if self.orientation_aircraft != 0:
                return self.turn_0()
            if self.aircraft.vx < 0:
                return pygame.K_UP

        if self.orientation_aircraft != 270:
            return self.turn_270()
        if self.aircraft.vy > 19:
            return pygame.K_UP
