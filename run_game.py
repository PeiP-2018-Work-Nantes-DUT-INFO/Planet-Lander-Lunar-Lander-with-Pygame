"""
The main function is defined here. It simply creates an instance of
tools.Control and adds the game states to its state_machine dictionary.
There should be no need (theoretically) to edit the tools.Control class.
All modifications should occur in this module
and in the prepare module.
"""

import tools
import pygame
from game_config import GameConfig
from components.debug import init_global
from states import splash, game
from states.demo import demo
from os import path


def main():
    """Add states to control here."""
    pygame.init()
    _screen = None
    if GameConfig.ENABLE_FULLSCREEN:
        _screen = pygame.display.set_mode((GameConfig.WINDOW_W, GameConfig.WINDOW_H), pygame.FULLSCREEN)
    else:
        _screen = pygame.display.set_mode((GameConfig.WINDOW_W, GameConfig.WINDOW_H))
    pygame.display.set_caption(GameConfig.CAPTION_WINDOW)

    _screen.fill(GameConfig.BACKGROUND_COLOR)
    _render = pygame.font.Font(None, 100).render("LOADING...", 0, pygame.Color("white"))
    _screen.blit(_render, _render.get_rect(center=GameConfig.SCREEN_RECT.center))
    pygame.display.update()

    pygame.mixer.music.load(path.join('ressources', 'music.mp3'))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

    init_global()

    app = tools.Control(GameConfig.CAPTION_WINDOW)
    state_dict = {"SPLASH": splash.Splash(),
                  "GAME": game.Game(),
                  "DEMO": demo.Demo()
                  }
    app.state_machine.setup_states(state_dict, "SPLASH")
    app.main()


main()
