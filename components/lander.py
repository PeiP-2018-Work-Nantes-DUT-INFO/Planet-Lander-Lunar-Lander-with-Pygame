import pygame
import math
from random import randint
from game_config import GameConfig


class Lander(pygame.sprite.DirtySprite):
    def __init__(self):
        super(pygame.sprite.DirtySprite, self).__init__()
        self.image = GameConfig.LANDER_IMG
        self.image = pygame.transform.rotate(self.image, -90)
        self.original = self.image
        self.score = 0
        self.rect = self.image.get_rect()
        self.rect.center = (15, 20)

        self.x = self.rect.center[0]
        self.y = self.rect.center[1]
        self.vx = LanderConfig.initialVelocityX
        self.vy = LanderConfig.initialVelocityY

        self.m = 5
        self.engine_power = 16.22 * self.m
        self.forceAcceleration = [0, 0]

        self.orientation = -180.0
        self.fuel = LanderConfig.INITIAL_FUEL
        self.landed = False
        self.landed_in_grace = False
        self.explodeDelay = 0
        self.finished_animation = False

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
        if self.landed:
            return
        self.orientation += angle

    ''' function landing_in_grace : 
            Usage : 
                - 
            Arguments : 
                - self : objet courant 
    '''

    def landing_in_grace(self):
        return (-100 < self.orientation < -80) and math.fabs(self.vy) < LanderConfig.MAX_VELOCITY_VERTICAL_SAFE_LANDING \
               and math.fabs(self.vx) < LanderConfig.MAX_VELOCITY_HORIZONTAL_SAFE_LANDING

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
            plateforms = [plateform for plateform in collision if plateform.type == 1]

            if self.landing_in_grace() and len(plateforms) > 0:
                self.landed_in_grace = True
                plateform_coords = plateforms.pop().coords
                self.score = self.compute_score(plateform_coords)
            self.landed = True
            self.vx = 0
            self.vy = 0
            self.forceAcceleration = [0, 0]

    def explode(self, screen):
        if self.explodeDelay >= LanderConfig.explodeDuration:
            self.kill()
            self.finished_animation = True
            return
        for i in range(randint(20, 40)):
            pygame.draw.line(screen,
                             (randint(190, 255),
                              randint(0, 100),
                              randint(0, 100)),
                             self.rect.center,
                             (randint(0, GameConfig.WINDOW_W),
                              randint(0, GameConfig.WINDOW_H)),
                             randint(1, 3))
        self.explodeDelay += 1

    def compute_score(self, plateform):
        """
        Score multiplier *
        ([40000 * (Percentage of fuel remaining - 50%)] +
        [30000 * (|Vertical velocity| / Maximum vertical velocity for a safe landing)^2] +
        [30000 * (|horizontal velocity| / Maximum horizontal velocity for a safe landing)^2])
        :param plateform:
        :return:
        """
        bonusFuel = max(self.fuel / LanderConfig.INITIAL_FUEL - 0.5, 0.0)
        return round(plateform[3] * ((40000 * bonusFuel) +
                                     (30000 * (self.vy / LanderConfig.MAX_VELOCITY_VERTICAL_SAFE_LANDING)) +
                                     (30000 * (self.vx / LanderConfig.MAX_VELOCITY_HORIZONTAL_SAFE_LANDING))))


class LanderConfig:
    dt = 0.02
    gravity = 3.244  # 1.622 * 2

    initialVelocityX = 50
    initialVelocityY = 0.0
    explodeDuration = 150
    INITIAL_FUEL = 1000
    MAX_VELOCITY_HORIZONTAL_SAFE_LANDING = 10
    MAX_VELOCITY_VERTICAL_SAFE_LANDING = 20
