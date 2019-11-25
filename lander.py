import pygame
import math
from GameConfig import GameConfig


class Lander(pygame.sprite.DirtySprite):
    def __init__(self):
        super(pygame.sprite.DirtySprite, self).__init__()
        self.image = pygame.image.load('lander_normal.png')

        self.original = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (0, 20)
        self.x = self.rect.center[0]
        self.y = self.rect.center[1]

        self.vx = LanderConfig.initialVelocityX
        self.vy = LanderConfig.initialVelocityY
        self.m = 5
        self.orientation = -90.0

        self.fuel = 1000
        self.engine_power = 0.000000001622

    ''' function update
        Usage : 
            - Appel des différentes fonction de mise à jour. 
        Argument : 
            - self : classe courante
    '''
    def update(self):
        self.update_physic(0, LanderConfig.gravity * self.m)
        self.rect.center = (self.x, self.y)
        self.update_image()

    ''' function update_physic
    Usage : 
        - Met à jour les données physiques du vaisseau (accélération, vitesse, position)
    Arguments : 
        - self : classe courante
        - fx : force sur l'axe des absisses 
        - fy : force sur l'axe des ordonnées
    '''
    def update_physic(self, fx, fy):
        ax = fx / self.m    # ax : accélération en x
        ay = fy / self.m    # ay : accélération en y
        self.vx = self.vx + ax * LanderConfig.dt    # vx : vitesse actuelle en x
        self.vy = self.vy + ay * LanderConfig.dt    # vy : vitesse actuelle en y
        self.x = self.x + self.vx * LanderConfig.dt
        self.y = self.y + self.vy * LanderConfig.dt

    ''' function update_image : 
        Usage : 
            - Met à jour l'image grâce à la nouvelle orientation
        Arguments : 
            - self : classe courante   
    '''
    def update_image(self):
        center = self.rect.center
        self.image = pygame.transform.rotate(self.original, -1 * self.orientation)
        self.rect = self.image.get_rect(center=center)

    ''' function boost
        Usage : 
            - Conditions de défaite (absence de carbarant) 
            - On créé le vecteur liée à la propulsion du vaisseau
        Arguments : 
            - self : classe courante
    '''
    def boost(self):
        if not self.fuel:
            return
        self.fuel -= 1
        print(self.orientation)
        fx = self.engine_power + math.sin(math.radians(self.orientation))
        fy = self.engine_power + math.cos(math.radians(self.orientation))
        self.update_physic(fx, fy)

    ''' function rotate : 
        Usage : 
            - permet la rotation du vaisseau
        Arguments : 
            - self : classe courante
            - angle : angle de rotation pour le vaisseau   
    '''
    def rotate(self, angle):
        self.orientation += angle


class LanderConfig:
    dt = 0.5
    gravity = 0.0001622
    initialVelocityX = 0.5
    initialVelocityY = 0.0
