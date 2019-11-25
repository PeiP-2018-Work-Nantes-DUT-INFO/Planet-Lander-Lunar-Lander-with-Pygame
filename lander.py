import pygame
import math
from GameConfig import GameConfig


class Lander(pygame.sprite.DirtySprite):
    def __init__(self):
        super(pygame.sprite.DirtySprite, self).__init__()
        self.image = pygame.image.load('lander_normal.png')
        self.image = pygame.transform.rotate(self.image,-90)
        self.original = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (0, 20)
        self.x = self.rect.center[0]
        self.y = self.rect.center[1]
        self.vx = LanderConfig.initialVelocityX
        self.vy = LanderConfig.initialVelocityY
        self.m = 5
        self.orientation = -90.0
        self.fuel = 100
        self.engine_power = 166.22*self.m
        # self.engine_power = 0.000000001622

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
        ax = fx / self.m
        ay = fy / self.m
        self.vx = self.vx + ax * LanderConfig.dt
        self.vy = self.vy + ay * LanderConfig.dt
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
        # self.fuel -= 1
        print(math.radians(self.orientation))
        fx = self.engine_power * math.cos(math.radians(self.orientation))
        fy = self.engine_power * math.sin(math.radians(self.orientation))
        print(fx, fy)
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
    dt = 0.01
    # gravity = 16.22
    gravity = 0

    initialVelocityX = 50
    initialVelocityY = 0.0
