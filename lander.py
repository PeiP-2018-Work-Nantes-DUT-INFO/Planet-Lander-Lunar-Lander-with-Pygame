import pygame
import math


class Lander(pygame.sprite.DirtySprite):
    def __init__(self):
        super(pygame.sprite.DirtySprite, self).__init__()
        self.image = pygame.image.load('lander_normal.png')
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
        self.landed_succes = False

    ''' function update
        Usage : 
            - Appel des différentes fonction de mise à jour. 
        Argument : 
            - self : classe courant
    '''
    def update(self):
        self.update_physic(0 + self.forceAcceleration[0], LanderConfig.gravity * self.m + self.forceAcceleration[1])
        self.forceAcceleration = [0, 0]
        self.rect.center = (self.x, self.y)
        self.update_image()
        print("Speed:", self.vx, self.vy)

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

    ''' function check_landed : 
        Usage : 
            - 
        Arguments : 
            - self : objet courant 
            - surface : 
    '''
    def check_landed(self, window):
        if self.landed:
            return
        collision = pygame.sprite.collide_circle(self, window)
        if collision:
            self.landed = True
            if self.land_succefuly():  # && window.
                self.landed_succes = True
            else:
                self.landed_succes = False
        self.vx = 0
        self.vy = 0
        self.forceAcceleration = [0, 0]

    ''' function land_succefuly : 
            Usage : 
                - 
            Arguments : 
                - self : objet courant 
    '''
    def land_succefuly(self):
        return (self.orientation <10 or self.orientation > 350) and self.vy < 20


class LanderConfig:
    dt = 0.02
    gravity = 3.244  # 1.622 * 2

    initialVelocityX = 50
    initialVelocityY = 0.0
