import pygame
from os import path

# Définition des classes


class GameConfig:
    # Taille de la fenêtre
    WINDOW_W = 1400
    WINDOW_H = 700
    SCREEN_RECT = pygame.Rect((0, 0), (WINDOW_W, WINDOW_H))
    # Initlisation du lander et de sa taille
    LANDER_IMG = pygame.image.load(path.join('Ressources', 'lander_normal.png'))
    LANDER_IMG_W = 30
    LANDER_IMG_H = 30
    SPLASH_IMG = pygame.image.load(path.join('Ressources', 'splash.jpg'))
    # Initialisation des couleurs
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Mise en place de l'affichage
    HUDLEFT_TOP_LEFT = (30, 30)
    HUD_RIGHT_TOPLEFT = (WINDOW_W - 200, 30)
    FONTSIZE_HUD = 16

    CAPTION_WINDOW = "Space Lander"

    BACKGROUND_COLOR = 0
