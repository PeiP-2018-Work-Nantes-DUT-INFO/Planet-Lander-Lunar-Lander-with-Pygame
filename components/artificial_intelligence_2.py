from components.artificial_intelligence import ArtificialIntelligence
from operator import itemgetter
import pygame
from components.lander import LanderConfig


class ArtificialIntelligence2(ArtificialIntelligence):
    def __init__(self):
        ArtificialIntelligence.__init__(self)
        self.plateform_target = None
        self.plateform_target_rect = None
        self.locked = False
        self.updates = 0
        self.ylaunch = None
        self.to_low = False
        self.reverse_thrust = False

    def game_start(self, landing, aircraft):
        ArtificialIntelligence.game_start(self, landing, aircraft)
        plateforms = [plateform for plateform in self.landing.plateforms if plateform[0] > AIConfig.MIN_PLATEFORM_X]
        self.plateform_target = max(plateforms, key=itemgetter(3))
        self.plateform_target_rect = pygame.Rect(self.plateform_target[0], self.plateform_target[1],
                                                 self.plateform_target[2], 1)
        self.locked = False

        between = False
        for i in range(0, len(self.aircraft.projection_motion_trajectory) - 1):
            x_0, y_0 = self.aircraft.projection_motion_trajectory[i]
            x_1, y_1 = self.aircraft.projection_motion_trajectory[i + 1]
            if x_0 <= self.plateform_target_rect.centerx <= x_1:
                between = True
                middle = (y_1 + y_0) / 2
                if self.plateform_target_rect.centery - middle < AIConfig.MIN_HEIGHT \
                        or middle > self.plateform_target_rect.centery:
                    self.to_low = True
        if not between:
            self.to_low = True

    def changed_state(self):
        pass

    def calculate_minimum_distance_y(self):
        i = 0
        depassed = False
        ylaunch = 0
        while not depassed:
            vy = self.aircraft.vy + LanderConfig.GRAVITY * i
            dy = 0.5 * LanderConfig.GRAVITY * (i ** 2) + self.aircraft.vy * i
            minimum_distance = (vy ** 2) / (2 * (self.aircraft.engine_power - LanderConfig.GRAVITY))
            if self.aircraft.rect.centery + dy + minimum_distance > self.plateform_target_rect.top:
                depassed = True
                ylaunch = self.plateform_target_rect.top - minimum_distance
                print('Minimum distance: ', minimum_distance)
                print('Vy: ', vy)
                print('Dy: ', vy)
                print('i', i)
            else:
                i += LanderConfig.DT
        return ylaunch, i

    def get_next_command(self, now):
        keys = [0, ] * 323
        will_collide = self.aircraft.will_collide_with_land_before_plateform(self.landing.landingStroke,
                                                                             self.plateform_target)
        if will_collide and not self.reverse_thrust:
            self.to_low = True
        if self.to_low and not (-90 <= self.aircraft.orientation <= -90):
            if -270 <= self.aircraft.orientation < -90:
                keys[pygame.K_RIGHT] = 1
            else:
                keys[pygame.K_LEFT] = 1
        if will_collide and not self.locked and (-90 <= self.aircraft.orientation <= -90):
            keys[pygame.K_UP] = 1

        if self.to_low and (-90 <= self.aircraft.orientation <= -90):
            for i in range(0, len(self.aircraft.projection_motion_trajectory) - 1):
                x_0, y_0 = self.aircraft.projection_motion_trajectory[i]
                x_1, y_1 = self.aircraft.projection_motion_trajectory[i + 1]
                if x_0 <= self.plateform_target_rect.centerx <= x_1:
                    middle = (y_1 + y_0) / 2
                    if self.plateform_target_rect.centery - middle < AIConfig.MIN_HEIGHT or\
                            middle > self.plateform_target_rect.centery:
                        keys[pygame.K_UP] = 1
                    else:
                        self.to_low = False
        minimum_distance = (self.aircraft.vx ** 2) / (2 * self.aircraft.engine_power)
        if self.aircraft.x + minimum_distance > self.plateform_target_rect.centerx and not self.locked:
            keys[pygame.K_UP] = 1
            self.reverse_thrust = True
            if round(self.aircraft.vx) == 0.0:
                self.locked = True

        if not self.reverse_thrust and not self.locked and not (
                -180 <= self.aircraft.orientation <= -180) and not self.to_low:
            if 0 <= self.aircraft.orientation < -180:
                keys[pygame.K_RIGHT] = 1
            else:
                keys[pygame.K_LEFT] = 1

        if self.locked and not (-90 <= self.aircraft.orientation <= -90):
            if -270 <= self.aircraft.orientation < -90:
                keys[pygame.K_RIGHT] = 1
            else:
                keys[pygame.K_LEFT] = 1

        if self.locked and not self.ylaunch:
            self.ylaunch, consumption = self.calculate_minimum_distance_y()

        if self.ylaunch:
            print('Aircraft state', self.aircraft.rect.centery, self.ylaunch)
            print('Plateform top:', self.plateform_target_rect.top)
            if self.aircraft.rect.centery >= self.ylaunch:
                keys[pygame.K_UP] = 1

        return keys

    def game_over(self):
        pass

    def win(self):
        pass


class AIConfig:
    THRESHOLD = 20
    MIN_HEIGHT = 300
    MIN_PLATEFORM_X = 200
