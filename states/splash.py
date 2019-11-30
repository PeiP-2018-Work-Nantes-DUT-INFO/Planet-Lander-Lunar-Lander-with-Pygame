"""
The splash screen of the game. The first thing the user sees.
"""

import pygame as pg

from game_config import GameConfig
import state_machine


class Splash(state_machine.State):
    """This State is updated while our game shows the splash screen."""

    def __init__(self):
        state_machine.State.__init__(self)
        self.next = "GAME"
        self.timeout = 5
        self.alpha = 0
        self.alpha_speed = 2  # Alpha change per frame
        self.image = GameConfig.SPLASH_IMG
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=GameConfig.SCREEN_RECT.center)

    def update(self, keys, now):
        """Updates the splash screen."""
        self.now = now
        self.alpha = min(self.alpha + self.alpha_speed, 255)
        self.image.set_alpha(self.alpha)
        if self.now - self.start_time > 1000.0 * self.timeout:
            self.done = True

    def draw(self, surface, interpolate):
        surface.fill(GameConfig.BACKGROUND_COLOR)
        surface.blit(self.image, self.rect)

    def get_event(self, event):
        """
        Get events from Control. Changes to next state on any key press.
        """
        self.done = event.type == pg.KEYDOWN
