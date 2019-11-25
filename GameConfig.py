import pygame
from pygame.mixer import Sound

# Définition des classes


class GameConfig:
    # Taille de la fenêtre
    windowW = 1400
    windowH = 700

    # Initlisation du lander et de sa taille
    lander = pygame.image.load('lander_normal.png')
    imgLanderW = 30
    imgLanderH = 30

    # Initialisation des couleurs
    white = (255, 255, 255)
    red = (255, 0, 0)

    # Mise en place de l'affichage
    hudLeftTopLeft = (30, 30)
    hudRightTopRight = (windowW - 200, 30)
    fontSizeHud = 16

    #Ajout d'une musique
    # music = Sound()
    # music.read('interstellar-main-theme-retro.mp3')
