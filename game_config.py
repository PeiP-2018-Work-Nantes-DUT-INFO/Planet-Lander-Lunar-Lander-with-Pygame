import pygame
from os import path

pygame.display.init()  # nécessaire pour déterminer la taille de l'écran


# Selon la doc, ce n'est pas grave de l'appeller plusieurs fois


# Définition des classes

class GameConfig:
    # Si à vrai, le jeu va démarrer en fullscreen
    ENABLE_FULLSCREEN = False

    # Taille de la fenêtre
    WINDOW_W_WINDOWED = 1400
    WINDOW_H_WINDOWED = 700

    # prend la taille de l'écran si en fullscreen
    WINDOW_W = pygame.display.Info().current_w if ENABLE_FULLSCREEN else WINDOW_W_WINDOWED
    WINDOW_H = pygame.display.Info().current_h if ENABLE_FULLSCREEN else WINDOW_H_WINDOWED
    SCREEN_RECT = pygame.Rect((0, 0), (WINDOW_W, WINDOW_H))

    # Initlisation du lander et de sa taille
    LANDER_IMG = pygame.image.load(path.join('ressources', 'lander_normal.png'))
    LANDER_IMG_W = 30
    LANDER_IMG_H = 30

    # Répresente l'image au début du jeu
    SPLASH_IMG = pygame.image.load(path.join('ressources', 'splash.jpg'))
    # Initialisation des couleurs
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Coordonnées de l'affichage (score, altitude, etc).
    HUDLEFT_TOP_LEFT = (30, 30)
    HUD_RIGHT_TOPLEFT = (WINDOW_W - round(WINDOW_W * 0.1786), 30)
    FONTSIZE_HUD = round(WINDOW_W * 0.0143)

    # Nom de la fenêtre
    CAPTION_WINDOW = "Space Lander"

    # Couleur de fond, 0 = noir
    BACKGROUND_COLOR = 0

    TEXT_INITIAL_PLAY = "INSERT COINS WITH ARROW KEYS\n\nPRESS ENTER TO PLAY\nARROW KEYS TO MOVE\n\n" \
                        "PRESS I TO LAUNCH AI"
    TEXT_DESTROYED_FUEL_REMAINING = "AUXILIARY FUEL\nTANKS DESTROYED\n{} FUEL UNITS LOST\n" \
                                    "YOU CREATED A TWO MILE CRATER"
    TEXT_GAME_OVER = "OUT OF FUEL\nGAME OVER\n\nYOU SCORE IS {}"
    TEXT_LOW_FUEL = "LOW ON FUEL"
    TEXT_NO_MORE_FUEL = "OUT OF FUEL"
    TEXT_CONGRATULATION = "CONGRATULATIONS\nA PERFECT LANDING\n{} POINTS"
    FONTSIZE_CENTER_TEXT = round(WINDOW_W * 0.0257)
    OFFSET_Y_CENTER_TEXT = round(WINDOW_H * 0.285)
    COLOR_CENTER_TEXT = WHITE
    BLINKING_CENTER_TEXT = 3000
    VERSION_TEXT = "v1.2-f"
    # temps avant de lancer la démo
    TIME_SECONDS_BEFORE_DEMO = 30
