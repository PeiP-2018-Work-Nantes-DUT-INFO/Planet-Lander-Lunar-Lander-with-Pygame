import pygame
from game_config import GameConfig

debug_group = None
debug_sprite_dynamic = None
debug_sprite_fixed = None


class DebugSprite(pygame.sprite.Sprite):
    def __init__(self, fixed):
        pygame.sprite.Sprite.__init__(self)
        self.type = 2
        self.image = pygame.Surface([GameConfig.WINDOW_W, GameConfig.WINDOW_H], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.fixed = fixed

    def update(self):
        if not self.fixed:
            self.image.fill((0, 0, 0, 0))

    def reset(self):
        self.image.fill((0, 0, 0, 0))


def init_global():
    global debug_group
    debug_group = pygame.sprite.Group()
    global debug_sprite_dynamic
    debug_sprite_dynamic = DebugSprite(False)
    global debug_sprite_fixed
    debug_sprite_fixed = DebugSprite(True)
    debug_group.add(debug_sprite_dynamic, debug_sprite_fixed)
