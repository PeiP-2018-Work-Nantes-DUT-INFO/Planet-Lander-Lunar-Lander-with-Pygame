# chargement des modules externes
import pygame
import state_machine
from tools import Timer
from game_config import GameConfig
from states.game import Game, render_text_center
from states.demo.credits import Credits


class Demo(state_machine.State):

    def __init__(self):
        state_machine.State.__init__(self)
        self.state_machine = state_machine.StateMachine()
        self.should_flip = False
        self.timer_delay = None
        self.blink = True

    def startup(self, now, persistant):
        self.state_machine.setup_states({
            'GAME': Game(),
            'CREDITS': Credits()
        }, 'CREDITS')
        self.state_machine.state.startup(now, persistant)
        self.should_flip = False
        self.blink = True
        self.timer_delay = Timer(1000)

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.done = True
            self.next = 'GAME'
            self.state_machine.state.cleanup()

    def update(self, keys, now):
        if self.state_machine.state_name == 'GAME' and not self.state_machine.state.AI:
            if not self.should_flip:
                self.state_machine.state_dict['GAME'].AI = True
                self.should_flip = True
                self.state_machine.state_dict['GAME'].restart_game_state()
            else:
                self.should_flip = False
                self.state_machine.state.next = 'CREDITS'
                self.state_machine.flip_state()

        self.state_machine.update(keys, now)
        if self.timer_delay.check_tick(now):
            self.blink = not self.blink

    def draw(self, surface, interpolate):
        self.state_machine.draw(surface, interpolate)
        if self.blink:
            render_text_center(surface,
                               '{} VERSION {}\nPRESS ANY KEYS TO START'.format(GameConfig.CAPTION_WINDOW.capitalize(),
                                                                               GameConfig.VERSION_TEXT.capitalize()),
                               GameConfig.COLOR_CENTER_TEXT,
                               GameConfig.WINDOW_H - GameConfig.FONTSIZE_CENTER_TEXT * 2,
                               GameConfig.FONTSIZE_CENTER_TEXT)
