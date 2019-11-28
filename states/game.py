# chargement des modules externes
import pygame

import state_machine
from tools import Timer
from game_config import GameConfig
from components.landing import Landing, LandingConfig
from components.lander import Lander, LanderConfig
from os import path

# Définition des classes
''' class Move
    Usage : 
        - permet la rotation du vaisseau
        - les valeurs de turn_left et turn_right sont en degré
'''


class Move:
    turn_left = -2
    turn_right = 2


# Définition des fonctions


def drawHUD(window, lander, score):
    ''' function drawHUD
        Usage :
            - affichage du score, du carburant et des données de vol
        Argument :
            - window : fenêtre de jeux
            - lander : information sur le vaisseau
            - score : score de la partie
    '''
    font = pygame.font.Font(path.join('ressources', 'Bender_Light.otf'), GameConfig.FONTSIZE_HUD)
    offset = 0

    for i in [('SCORE : {0:04d}', score), ('FUEL : {0:03d}', max(0, lander.fuel))]:
        img = font.render(i[0].format(i[1]), True, GameConfig.WHITE)
        display_rect = img.get_rect()
        display_rect.topleft = (GameConfig.HUDLEFT_TOP_LEFT[0], GameConfig.HUDLEFT_TOP_LEFT[1] + offset)
        window.blit(img, display_rect)
        offset += GameConfig.FONTSIZE_HUD
    offset = 0
    for i in [('ALTITUDE : {0:04.0f}', GameConfig.WINDOW_H - lander.y), ('HORIZONTAL SPEED: {0:.0f}', lander.vx,),
              ('VERTICAL SPEED: {0:.0f}', lander.vy)]:
        img = font.render(i[0].format(i[1]), True, GameConfig.WHITE)
        display_rect = img.get_rect()
        display_rect.topleft = (GameConfig.HUD_RIGHT_TOPLEFT[0], GameConfig.HUD_RIGHT_TOPLEFT[1] + offset)
        window.blit(img, display_rect)
        offset += GameConfig.FONTSIZE_HUD


def render_text_center(surface, string, color, start_y, y_space):
    """
    Takes a list of strings and returns a list of
    (rendered_surface, rect) tuples. The rects are centered on the screen
    and their y coordinates begin at starty, with y_space pixels between
    each line.
    """
    font = pygame.font.Font(path.join('ressources', 'Bender_Light.otf'), GameConfig.FONTSIZE_CENTER_TEXT)
    rendered_text = []
    for i, string in enumerate(string.splitlines()):
        msg_center = (GameConfig.SCREEN_RECT.centerx, start_y + i * y_space)
        msg_data = render_font(font, string, color, msg_center)
        rendered_text.append(msg_data)
    for msg in rendered_text:
        surface.blit(msg[0], msg[1])


def render_font(font, msg, color, center):
    """Returns the rendered font surface and its rect centered on center."""
    msg = font.render(msg, 1, color)
    rect = msg.get_rect(center=center)
    return msg, rect


''' function gameloop
    Usage : 
        - fonction principale du jeux
    Arguments : 
        - window : fenêtre de jeux
        - horloge : variable permettant de gérer le taux de rafraichissement par seconde
'''


class Game(state_machine._State):
    """Core state for the actual gameplay."""

    def __init__(self):
        state_machine._State.__init__(self)
        self.land = None
        self.aircraft = None
        self.aircraft_team = None
        self.timer = None
        self.reset_game = True
        self.reset_map = False
        self.state = "IDLE"
        self.blink = True
        self.AI = False
        self.fuel = 0
        self.score = 0
        self.timer_display_message = None
        self.display_message = ''

    def startup(self, now, persistant):
        """
        Call the parent class' startup method.
        If reset_map has been set (after player death etc.) recreate the world
        map and reset relevant variables.
        """
        state_machine._State.startup(self, now, persistant)
        if not 'draw_debug' in self.persist:
            self.persist = {
                "number_of_plateforms": LandingConfig.numberOfPlateforms,
                "initial_fuel": LanderConfig.INITIAL_FUEL,
                "draw_debug": False
            }
        if self.reset_game:
            LandingConfig.drawDebug = self.persist['draw_debug']
            LandingConfig.numberOfPlateforms = self.persist['number_of_plateforms']
            LanderConfig.INITIAL_FUEL = self.persist['initial_fuel']
            self.score = 0
            self.fuel = LanderConfig.INITIAL_FUEL
            self.state = 'INTRO'
            self.AI = False
            self.blink = True
            self.timer = Timer(GameConfig.BLINKING_CENTER_TEXT)
        if self.reset_game or self.reset_map:
            self.reset_game = False
            self.reset_map = False
            self.land = Landing()
        self.aircraft = Lander()
        self.aircraft.fuel = self.fuel
        self.timer_display_message = Timer(2000)
        self.aircraft_team = pygame.sprite.Group(self.aircraft)

    def cleanup(self):
        """Store background color and sidebar for use in camp menu."""
        self.done = False
        return self.persist

    def restart_game_state(self, reset_map=False):
        self.done = True
        self.state = 'INGAME'
        self.next = "GAME"
        self.blink = False
        self.reset_map = reset_map

    def reset_game_state(self):
        self.done = True
        self.state = 'INTRO'
        self.reset_game = True
        self.next = "GAME"

    def get_event(self, event):
        """
        Process game state events. Add and pop directions from the player's
        direction stack as necessary.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.reset_game_state()
            if self.state == 'INTRO':
                if event.key == pygame.K_RETURN:
                    self.AI = False
                if event.key == pygame.K_i:
                    self.AI = True
                if event.key in (pygame.K_i, pygame.K_RETURN):
                    self.restart_game_state()
                if event.key in (pygame.K_d, pygame.K_u, pygame.K_j):
                    self.reset_game_state()
                if event.key == pygame.K_d:
                    self.persist['draw_debug'] = not self.persist['draw_debug']
                elif event.key == pygame.K_u:
                    self.persist['number_of_plateforms'] += 1
                elif event.key == pygame.K_j:
                    self.persist['number_of_plateforms'] -= 1
                elif event.key == pygame.K_UP:
                    self.update_fuel(-200)
                    self.persist['initial_fuel'] = self.fuel
                elif event.key == pygame.K_DOWN:
                    self.update_fuel(200)
                    self.persist['initial_fuel'] = self.fuel

    def update_fuel(self, fuel):
        self.fuel -= fuel
        self.aircraft.fuel = self.fuel
        return self.game_over()

    def low_on_fuel(self, fuel):
        return self.fuel < 200

    def game_over(self):
        return self.fuel <= 0

    def update(self, keys, now):
        """Update phase for the primary game state."""
        self.now = now
        if self.state == 'INTRO' or (self.state == 'INGAME' and self.fuel < 200):
            if self.timer.check_tick(now):
                self.blink = not self.blink
            if self.state == 'INTRO':
                self.display_message = GameConfig.TEXT_INITIAL_PLAY
            elif self.state == 'INGAME' and self.fuel == 0:
                self.blink = True
                self.display_message = GameConfig.TEXT_NO_MORE_FUEL
            elif self.state == 'INGAME' and self.low_on_fuel(self.fuel):
                self.display_message = GameConfig.TEXT_LOW_FUEL

        if self.state == 'INGAME':
            if self.AI:
                keys = (0,) * 323
            if keys[pygame.K_LEFT]:
                self.aircraft.rotate(Move.turn_left)
            elif keys[pygame.K_RIGHT]:
                self.aircraft.rotate(Move.turn_right)
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.aircraft.boost()

        self.aircraft.check_collision(self.land.landingEntities)
        self.land.landingEntities.update()
        self.aircraft_team.update()
        self.fuel = self.aircraft.fuel
        if self.aircraft.landed:
            self.update_landed(now)
        else:
            self.timer_display_message.timer = now

    def update_landed(self, now):
        if not self.aircraft.landed_in_grace:
            if self.state == 'INTRO' and self.aircraft.finished_animation:
                self.next = 'GAME'
                self.done = True
            if self.state in ('INGAME', 'WAITDIE'):
                if self.state != 'WAITDIE' and not self.aircraft.finished_animation:
                    self.state = 'WAITDIE'
                    if not self.update_fuel(200):
                        self.display_message = GameConfig.TEXT_DESTROYED_FUEL_REMAINING.format(200)
                    else:
                        self.display_message = GameConfig.TEXT_GAME_OVER
                    self.blink = True
                elif self.aircraft.finished_animation:
                    if self.game_over():
                        self.reset_game_state()
                    else:
                        self.restart_game_state()
        else:
            if not self.timer_display_message.check_tick(now):
                self.display_message = GameConfig.TEXT_CONGRATULATION.format(self.aircraft.score)
                self.blink = True
            else:
                self.score += self.aircraft.score
                self.restart_game_state(True)

    def draw(self, surface, interpolate):
        """Draw level and sidebar; if player is dead draw death sequence."""
        surface.fill(GameConfig.BACKGROUND_COLOR)
        self.land.landingEntities.draw(surface)
        self.aircraft_team.draw(surface)
        if self.aircraft.landed:
            if not self.aircraft.landed_in_grace:
                self.aircraft.explode(surface)
        drawHUD(surface, self.aircraft, self.score)
        if self.blink:
            render_text_center(surface, self.display_message, GameConfig.COLOR_CENTER_TEXT,
                               GameConfig.OFFSET_Y_CENTER_TEXT,
                               GameConfig.FONTSIZE_CENTER_TEXT)
