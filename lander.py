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
        self.fuel = 100
        self.engine_power = 0.000000001622

    def update_physic(self, fx, fy):
        ax = fx / self.m
        ay = fy / self.m
        self.vx = self.vx + ax * LanderConfig.dt
        self.vy = self.vy + ay * LanderConfig.dt
        self.x = self.x + self.vx * LanderConfig.dt
        self.y = self.y + self.vy * LanderConfig.dt

    def boost(self):
        if not self.fuel: return
        self.fuel -= 1
        print(self.orientation)
        fx = self.engine_power + math.sin(math.radians(self.orientation))
        fy = self.engine_power + math.cos(math.radians(self.orientation))
        self.update_physic(fx, fy)

    def update_image(self):
        center = self.rect.center
        self.image = pygame.transform.rotate(self.original, -1 * self.orientation)
        self.rect = self.image.get_rect(center=center)

    def update(self):
        self.update_physic(0, LanderConfig.gravity * self.m)
        self.rect.center = (self.x, self.y)
        self.update_image()

    def rotate(self, angle):
        self.orientation += angle


class LanderConfig:
    dt = 4
    gravity = 0.0001622
    initialVelocityX = 0.5
    initialVelocityY = 0.0
