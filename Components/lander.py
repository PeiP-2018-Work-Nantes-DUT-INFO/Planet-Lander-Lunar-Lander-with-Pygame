import pygame
import math
from random import randint
from GameConfig import GameConfig


class Lander(pygame.sprite.DirtySprite):
    def __init__(self):
        super(pygame.sprite.DirtySprite, self).__init__()
        self.image = GameConfig.lander
        self.image = pygame.transform.rotate(self.image, -90)
        self.original = self.image

        self.rect = self.image.get_rect()
        self.rect.center = (0, 20)

        self.x = self.rect.center[0]
        self.y = self.rect.center[1]
        self.vx = LanderConfig.initialVelocityX
        self.vy = LanderConfig.initialVelocityY

        self.m = 5
        self.engine_power = 16.22 * self.m
        self.forceAcceleration = [0, 0]

        self.orientation = -180.0
        self.fuel = 1000
        self.landed = False
        self.landed_in_grace = False
        self.explodeDelay = 0

    ''' function update
        Usage : 
            - Appel des différentes fonction de mise à jour. 
        Argument : 
            - self : classe courant
    '''

    def update(self):
        if not self.landed:
            self.update_physic(0 + self.forceAcceleration[0], LanderConfig.gravity * self.m + self.forceAcceleration[1])
        self.forceAcceleration = [0, 0]
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
            - self : objet courante  
    '''

    def update_image(self):
        center = self.rect.center
        self.image = pygame.transform.rotate(self.original, -1 * self.orientation)
        self.rect = self.image.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.image, 0)

    ''' function boost
        Usage : 
            - Conditions de défaite (absence de carbarant) 
            - On créé le vecteur liée à la propulsion du vaisseau
        Arguments : 
            - self : objet courant
    '''

    def boost(self):
        if not self.fuel:
            return
        self.fuel -= 1
        self.forceAcceleration = [self.engine_power * math.cos(math.radians(self.orientation)),
                                  self.engine_power * math.sin(math.radians(self.orientation))]

    ''' function rotate : 
        Usage : 
            - permet la rotation du vaisseau
        Arguments : 
            - self : objet courant 
            - angle : angle de rotation pour le vaisseau   
    '''

    def rotate(self, angle):
        self.orientation += angle

    ''' function land_succefuly : 
            Usage : 
                - 
            Arguments : 
                - self : objet courant 
    '''

    def landing_in_grace(self):
        return (-100 < self.orientation < -80) and math.fabs(self.vx) < 20

    ''' function check_landed : 
        Usage : 
            - 
        Arguments : 
            - self : objet courant 
            - surface : 
    '''

    def check_collision(self, landing_group):
        if self.landed:
            return
        collision = pygame.sprite.spritecollide(self, landing_group, False, collided=pygame.sprite.collide_mask)
        if collision:
            self.landed_in_grace = self.landing_in_grace()
            self.landed = True
            self.vx = 0
            self.vy = 0
            self.forceAcceleration = [0, 0]

    def explode(self, screen):
        if self.explodeDelay >= LanderConfig.explodeDuration:
            self.kill()
            return
        for i in range(randint(20, 40)):
            pygame.draw.line(screen,
                             (randint(190, 255),
                              randint(0, 100),
                              randint(0, 100)),
                             self.rect.center,
                             (randint(0, GameConfig.windowW),
                              randint(0, GameConfig.windowH)),
                             randint(1, 3))
        self.explodeDelay+=1


class LanderConfig:
    dt = 0.02
    gravity = 3.244  # 1.622 * 2

    initialVelocityX = 50
    initialVelocityY = 0.0
    explodeDuration = 100
