import math
import pygame

# Définition des classes


class Vecteur:
    def __init__(self, x, y, angle=None, norme=None):
        # Constructeurs
        self.x = x
        self.y = y

        if angle is not None and norme is not None:
            self.x = norme + math.sin(math.radians(angle))
            self.y = norme + math.cos(math.radians(angle))

        @property  # Permet de définir la norme
        def norme(self):
            return math.sqrt(self.x**2 + self.y**2)

        @property  # Permet de définir l'angle
        def angle(self):
            if math.floor(self.y == 0):  # On met le Math.floor uniquement ici pour éviter d'avoir une norme en (0,0)
                if self.x > 0:
                    return 90.0
                else:
                    return 270.0
            elif self.x:
                if self.y > 0:
                    return 180.0
                else:
                    return 0.0
            else:
                return math.degrees(math.tan(self.x/self.y))

        # Méthodes de classe
        def __add__(self, newVecteur):
            return Vecteur(x=(self.x + newVecteur.x), y=(self.y + newVecteur.y))

        def __str__(self):
            return "X: %.3d Y: %.3d Angle: %.3d degrees Norme: %.3d" % (self.x, self.y, self.angle, self.norme)

