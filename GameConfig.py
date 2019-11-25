# Définition des classes
import pygame


class GameConfig:
    # Taille de la fenêtre
    windowW = 1500
    windowH = 700

    # Initlisation du lander et de sa taille
    lander = pygame.image.load('lander_normal.png')
    imgLanderW = 30
    imgLanderH = 30
    white = (255, 255, 255)
    red = (255, 0, 0)
    hudLeftTopLeft = (30, 30)
    hudRightTopRight = (windowW - 200, 30)
    fontSizeHud = 20
