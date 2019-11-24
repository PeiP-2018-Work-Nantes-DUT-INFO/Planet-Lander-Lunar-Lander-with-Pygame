# Modules externes
import pygame


# Classes
class Gameconfig :
    white = (255, 255, 255)

    windowH = 1300
    windowW = 700

    imgLander = pygame.image.load('585f9635cb11b227491c3589.png')
    landerH = 50
    landerW = 50


class GameState:
    def __init__(self):
        self.landerModuleX = 100
        self.landerModuleY = 100

    def draw(self, window):
        window.blit(Gameconfig.imgLander, (self.landerModuleX, self.landerModuleY))

# Fonctions


def gameLoop(window) : #Boucle de jeu
    game_over = False
    gameState = GameState()

    while not game_over:
        gameState.draw(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        pygame.display.update()

def main(): #Fonction principale
    pygame.init()
    window = pygame.display.set_mode((Gameconfig.windowH, Gameconfig.windowW))
    pygame.display.set_caption("Planet Lander")

    gameLoop(window)
    pygame.quit()
    quit()


#Execution fonction principale
main()
