import pygame
import math
from random import randint
from game_config import GameConfig
import components.debug as debug


class Lander(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        rect_img = GameConfig.LANDER_IMG.get_rect()
        self.image = pygame.Surface((rect_img.size[0] + 30, rect_img.size[1] + 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        rect_img.center = self.rect.center
        self.image.blit(GameConfig.LANDER_IMG, rect_img)
        self.image = pygame.transform.rotate(self.image, -90)
        self.original = self.image
        self.score = 0
        self.rect.center = (20, 20)

        self.x = self.rect.center[0]
        self.y = self.rect.center[1]
        self.vx = LanderConfig.INITIAL_VELOCITY_X
        self.vy = LanderConfig.INITIAL_VELOCITY_Y

        self.m = 5
        self.engine_power = 16.22
        self.forceAcceleration = [0, 0]

        self.orientation = -180
        self.fuel = LanderConfig.INITIAL_FUEL
        self.landed = False
        self.landed_in_grace = False
        self.explode_delay = 0
        self.finished_animation = False
        self.boost_amount = 0
        self.mask = pygame.mask.from_surface(self.image, 127)
        self.boost_delay = 0

        self.projection_motion_trajectory = []
        self.invisible_trajectory = InvisibleTrajectory()
        self.update_trajectory()

    def update(self):
        """
        Usage :
            - Appel des différentes fonction de mise à jour.
        """
        if self.boost_amount:
            self.boost_delay += 1
        if self.boost_amount >= 0:
            self.boost_amount -= math.sqrt(self.boost_delay)
        else:
            self.boost_delay = 0
            self.boost_amount = 0

        if not self.landed:
            self.update_physic(0 + self.forceAcceleration[0], LanderConfig.GRAVITY * self.m + self.forceAcceleration[1])
            if math.fabs(self.forceAcceleration[0]) > 0 or math.fabs(self.forceAcceleration[1]) > 0:
                self.update_trajectory()
        self.forceAcceleration = [0, 0]
        self.rect.center = (self.x, self.y)
        self.update_image()
        if LanderConfig.DRAW_PROJECTION_TRACE:
            self.draw_trajectory()

    def update_trajectory(self):
        self.projection_motion_trajectory = []
        for i in range(1, 500, 1):
            self.projection_motion_trajectory.append((self.vx * i + self.x,
                                                      0.5 * LanderConfig.GRAVITY * (i ** 2) + self.vy * i + self.y
                                                      ))
        self.invisible_trajectory.update(self.projection_motion_trajectory)

    def draw_trajectory(self):
        for (x, y) in self.projection_motion_trajectory:
            pygame.draw.circle(debug.debug_sprite_dynamic.image, GameConfig.WHITE,
                               [int(x), int(y)],
                               4, 4)
            # debug.debug_sprite_fixed.image.blit(self.invisible_trajectory.image, self.invisible_trajectory.rect)

    def update_physic(self, fx, fy):
        """
        Usage :
            - Met à jour les données physiques du vaisseau (accélération, vitesse, position)
        :param fx: force sur l'axe des absisses
        :param fy: force sur l'axe des ordonnées
        """
        ax = fx / self.m
        ay = fy / self.m
        self.vx = self.vx + ax * LanderConfig.DT
        self.vy = self.vy + ay * LanderConfig.DT
        self.x = self.x + self.vx * LanderConfig.DT
        self.y = self.y + self.vy * LanderConfig.DT

    def update_boost(self):
        """
        Usage :
            - Met à jour l'image de la flamme
        """
        length_flame = round((self.boost_amount / LanderConfig.BOOST_INITIAL_AMOUNT) * LanderConfig.MAX_LENGTH_FLAME)
        center = (self.rect.w / 2, self.rect.h / 2)
        point_1 = rotate_point([center[0] - 4, 11 + center[1]], center, (self.orientation + 90) % 360)
        point_2 = rotate_point([center[0] + 4, 11 + center[1]], center, (self.orientation + 90) % 360)
        point_3 = rotate_point([center[0], length_flame + center[1] + 11], center, (self.orientation + 90) % 360)
        thrust_point = [point_1, point_2, point_3]
        pygame.draw.polygon(self.image, GameConfig.WHITE, thrust_point, 1)

    def update_image(self):
        center = self.rect.center
        self.image = pygame.transform.rotate(self.original, -1 * self.orientation)
        self.rect = self.image.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.image, 0)
        if self.boost_amount:
            self.update_boost()

    ''' function boost
        Usage : 
            - Conditions de défaite (absence de carbarant) 
            - On créé le vecteur liée à la propulsion du vaisseau
        Arguments : 
            - self : objet courant
    '''

    def boost(self):
        if not self.fuel or self.landed:
            return
        self.boost_delay = 0
        if self.boost_amount >= LanderConfig.BOOST_INITIAL_AMOUNT:
            self.boost_amount -= LanderConfig.OFFSET_FLAME
        else:
            self.boost_amount += LanderConfig.OFFSET_FLAME
        self.fuel -= 1
        self.forceAcceleration = [self.m * self.engine_power * math.cos(math.radians(self.orientation)),
                                  self.m * self.engine_power * math.sin(math.radians(self.orientation))]

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
        return (-100 < self.orientation < -80) and math.fabs(self.vy) < LanderConfig.MAX_VELOCITY_VERTICAL_SAFE_LANDING\
               and math.fabs(self.vx) < LanderConfig.MAX_VELOCITY_HORIZONTAL_SAFE_LANDING

    def will_collide_with_land_before_plateform(self, land, plateform):
        collision = pygame.sprite.collide_mask(self.invisible_trajectory, land)
        if collision:
            if self.x < plateform[0] + plateform[2] / 2:
                return collision[1] < plateform[1] and collision[0] < plateform[0]
            else:
                return collision[1] < plateform[1] and collision[0] > plateform[0]
        else:
            return False

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

        if collision or self.rect.right < 0 or self.rect.left > GameConfig.WINDOW_W:
            plateforms = [plateform for plateform in collision if plateform.type == 1]

            if self.landing_in_grace() and len(plateforms) > 0:
                self.landed_in_grace = True
                plateform_coords = plateforms.pop().coords
                self.score = self.compute_score(plateform_coords)
            self.landed = True
            self.boost_amount = 0
            self.vx = 0
            self.vy = 0
            self.forceAcceleration = [0, 0]

    def explode(self, screen):
        if self.explode_delay >= LanderConfig.EXPLOSION_DURATION:
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
        self.explode_delay += 1

    def compute_score(self, plateform):
        """
        Score multiplier *
        ([40000 * (Percentage of fuel remaining - 50%)] +
        [30000 * (|Vertical velocity| / Maximum vertical velocity for a safe landing)^2] +
        [30000 * (|horizontal velocity| / Maximum horizontal velocity for a safe landing)^2])
        :param plateform:
        :return:
        """
        bonus_fuel = max(self.fuel / LanderConfig.INITIAL_FUEL - 0.5, 0.0)
        return round(plateform[3] * ((40000 * bonus_fuel) +
                                     (30000 * (math.fabs(self.vy) / (
                                             LanderConfig.MAX_VELOCITY_VERTICAL_SAFE_LANDING ** 2))) +
                                     (30000 * (math.fabs(self.vx) / (
                                             LanderConfig.MAX_VELOCITY_HORIZONTAL_SAFE_LANDING ** 2)))))


def rotate_point(point, center, angle):
    angle = math.radians(angle)
    return (
        math.cos(angle) * (point[0] - center[0]) - math.sin(angle) * (point[1] - center[1]) + center[0],
        math.sin(angle) * (point[0] - center[0]) + math.cos(angle) * (point[1] - center[1]) + center[0]
    )


class InvisibleTrajectory(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface((GameConfig.WINDOW_W, GameConfig.WINDOW_H), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.points = []
        self.mask = None

    def update(self, points):
        self.points = points
        self.image.fill((0, 0, 0, 0))
        for i in range(0, len(points) - 1):
            pygame.draw.line(self.image, GameConfig.WHITE, points[i], points[i + 1], GameConfig.LANDER_IMG_H + 100)
        self.mask = pygame.mask.from_surface(self.image, 127)


class LanderConfig:
    DT = 0.02
    GRAVITY = 3.244  # 1.622 * 2
    INITIAL_VELOCITY_X = 50
    INITIAL_VELOCITY_Y = 0.0
    EXPLOSION_DURATION = 150
    INITIAL_FUEL = 1000
    MAX_VELOCITY_HORIZONTAL_SAFE_LANDING = 10
    MAX_VELOCITY_VERTICAL_SAFE_LANDING = 20
    MAX_LENGTH_FLAME = 20
    BOOST_INITIAL_AMOUNT = 50
    OFFSET_FLAME = 30
    DRAW_PROJECTION_TRACE = False
