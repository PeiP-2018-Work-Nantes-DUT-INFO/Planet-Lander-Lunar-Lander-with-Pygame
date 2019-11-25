import math
import pygame

# Définition des classes


class Vecteur:
    def __init__(self, x, y, angle, norme=None):
        self.x = x
        self.y = y

        if angle is not None and norme is not None: #Dans le cas ou le vaisseau est déjà soumis à un vecteur de force.
            self.x = norme + math.sin(math.radians(angle))
            self.y = norme + math.cos(math.radians(angle))

        @property
        def norme(self):
            return math.sqrt(self.x**2 + self.y**2)

        @property
        def angle(self):
            if math.floor(self.y == 0): #On met le Math.floor uniquement ici pour éviter d'avoir une norme en (0,0)
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