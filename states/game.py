# chargement des modules externes
import pygame

import state_machine
from game_config import GameConfig
from components.landing import Landing, LandingConfig
from components.lander import Lander
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
''' function drawHUD
    Usage : 
        - affichage du score, du carburant et des données de vol
    Argument : 
        - window : fenêtre de jeux
        - lander : information sur le vaisseau
        - score : score de la partie
'''


def drawHUD(window, lander, score):
    font = pygame.font.Font(path.join('ressources', 'Bender_Light.otf'), GameConfig.FONTSIZE_HUD)
    offset = 0

    for i in [('SCORE : {0:04d}', score), ('FUEL : {0:03d}', lander.fuel)]:
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
    font = pygame.font.Font(path.join('ressources', 'Bender_Light.otf'), GameConfig.CENTER_TEXT_FONTSIZE)
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
        self.reset_game = True
    def startup(self, now, persistant):
        """
        Call the parent class' startup method.
        If reset_map has been set (after player death etc.) recreate the world
        map and reset relevant variables.
        """
        state_machine._State.startup(self, now, persistant)
        if self.reset_game:
            self.land = Landing()
            self.score = 0
            self.fuel = 0
        self.aircraft = Lander()
        self.aircraft_team = pygame.sprite.Group(self.aircraft)

    def cleanup(self):
        """Store background color and sidebar for use in camp menu."""
        self.done = False
        return self.persist

    def get_event(self, event):
        """
        Process game state events. Add and pop directions from the player's
        direction stack as necessary.
        """

    def update(self, keys, now):
        """Update phase for the primary game state."""
        self.now = now
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
        if keys[pygame.K_LEFT]:
            self.aircraft.rotate(Move.turn_left)
        elif keys[pygame.K_RIGHT]:
            self.aircraft.rotate(Move.turn_right)
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.aircraft.boost()
        self.aircraft.check_collision(self.land.landingEntities)
        self.land.landingEntities.update()
        self.aircraft_team.update()

    def draw(self, surface, interpolate):
        """Draw level and sidebar; if player is dead draw death sequence."""
        surface.fill(GameConfig.BACKGROUND_COLOR)
        self.land.landingEntities.draw(surface)
        self.aircraft_team.draw(surface)
        if self.aircraft.landed:
            if not self.aircraft.landed_in_grace:
                self.aircraft.explode(surface)
        drawHUD(surface, self.aircraft, self.score)
        render_text_center(surface, "Test3232 3223\nTest222\nTes", GameConfig.WHITE, 300,
                           GameConfig.CENTER_TEXT_FONTSIZE)
