# chargement des modules externes
import pygame
import components.debug

import state_machine
from tools import Timer
from game_config import GameConfig
from components.landing import Landing, LandingConfig
from components.lander import Lander, LanderConfig
from states.game import render_text_center


class Credits(state_machine.State):

    def __init__(self):
        state_machine.State.__init__(self)
        self.land = None
        self.aircraft = None
        self.aircraft_team = None
        self.timer_delay = None
        self.draw_credits = False

        self.timer_display_message = None
        self.display_message = ''
        self.debug_group = components.debug.debug_group
        self.number_plateform_save = 0
        self.gravity_save = 0
        self.credit_index = 0

    def startup(self, now, persistant):
        state_machine.State.startup(self, now, persistant)
        self.number_plateform_save = LandingConfig.numberOfPlateforms
        self.gravity_save = LanderConfig.GRAVITY
        LanderConfig.GRAVITY = 0
        LandingConfig.numberOfPlateforms = 0
        self.draw_credits = False
        self.timer_delay = Timer(CreditConfig.DELAY_BETWEEN_CREDITS)
        self.land = Landing()
        self.aircraft = Lander()
        self.aircraft.fuel = 1000
        self.timer_display_message = Timer(CreditConfig.CREDIT_DURATION)
        self.aircraft_team = pygame.sprite.Group(self.aircraft)
        self.aircraft.orientation = 0
        self.credit_index = 0

    def cleanup(self):
        self.done = False
        LandingConfig.numberOfPlateforms = self.number_plateform_save
        LanderConfig.GRAVITY = self.gravity_save
        return self.persist

    def get_event(self, event):
        pass

    def update(self, keys, now):
        self.now = now
        self.debug_group.update()
        self.aircraft.boost()
        self.aircraft.vy = 0
        self.aircraft.vx = CreditConfig.SPEED_AIRCRAFT
        self.aircraft.y = CreditConfig.AIRCRAFT_Y_POS
        self.land.landingEntities.update()
        self.aircraft_team.update()
        self.aircraft.fuel = 1000
        if self.aircraft.rect.left > GameConfig.WINDOW_W:
            self.land = Landing()
            self.aircraft.x = - 15

        if not self.draw_credits:
            self.timer_display_message.timer = now
            if self.timer_delay.check_tick(now):
                self.draw_credits = not self.draw_credits
        else:
            self.timer_delay.timer = now
            if self.timer_display_message.check_tick(now):
                self.draw_credits = not self.draw_credits
                self.credit_index += 1
        if self.credit_index >= len(CreditConfig.CREDITS):
            self.done = True
            self.next = 'GAME'
        else:
            self.display_message = CreditConfig.CREDITS[self.credit_index]

    def draw(self, surface, interpolate):
        surface.fill(GameConfig.BACKGROUND_COLOR)
        self.land.landingEntities.draw(surface)
        self.aircraft_team.draw(surface)
        self.debug_group.draw(surface)
        if self.draw_credits:
            render_text_center(surface, self.display_message, GameConfig.COLOR_CENTER_TEXT,
                               CreditConfig.OFFSET_Y_CREDIT,
                               GameConfig.FONTSIZE_CENTER_TEXT)


class CreditConfig:
    CREDITS = [
        'CO-DEVELOPER: \nADAME NAJI',
        'CO-DEVELOPER:\nSIMON SASSI',
        'LIBS USED:\nPYGAME\nVISUALS FROM ATARI',
        'THANKS TO OUR TESTERS:\nALBERT GUIHARD',
        'THANKS TO OUR TESTERS:\nBAPTISTE BATARD',
        'WE DON''T FORGET THEM:\nVINCENT RICORDEL\nMATTIAS DUPUIS\nPHILIPPE RANNOU',
        'IUT DE NANTES 2019\nIT DEPARTMENT\nUNIVERSITY OF NANTES'
    ]
    CREDIT_DURATION = 6000
    DELAY_BETWEEN_CREDITS = 700
    OFFSET_Y_CREDIT = 300
    SPEED_AIRCRAFT = 200
    AIRCRAFT_Y_POS = 50
