# Modules externes
import pygame


# Classes
class Gameconfig :
    windowH = 1300
    windowW = 700


class GameState:
    def __init__(self):
        self.landerModuleX = 100
        self.landerModuleY = 100


# Fonctions


def gameLoop() : #Boucle de jeu
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True


def main(): #Fonction principale
    pygame.init()
    window = pygame.display.set_mode((Gameconfig.windowH, Gameconfig.windowW))

    gameLoop()
    pygame.quit()
    quit()


#Execution fonction principale
main()
