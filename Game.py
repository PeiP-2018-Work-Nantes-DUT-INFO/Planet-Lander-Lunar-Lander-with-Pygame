# chargement des modules externes
import pygame
from GameConfig import GameConfig
import landing
import time
from random import *



class GameState:
    def __init__(self):  # Placement du module au début du jeu
        self.landerX = 100
        self.landerY = 50
        self.angleLander = 0

    def draw(self, window):  # Affichage des différents composant sur la fenêtre
        window.blit(GameConfig.lander, (self.landerX, self.landerY))

    def advanceState(self, nextAngle):
        self.angleLander += nextAngle


class Move:
    Up = 5
    Down = -5
    TurnLeft = -5
    TurnRight = 5


# Fonctions du jeu
def blitRotate(surf, image, pos, originPos, angle):
    # Calculer la boîte de délimitation alignée sur l'axe de l'image en rotation
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # Calcule la translation autour du pivot
    pivot = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # Calculer l'origine en haut à gauche de l'image pivotée
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # Obtenir une image pivotée
    rotated_image = pygame.transform.rotate(image, angle)

    # faire pivoter et lisser l'image
    surf.blit(rotated_image, origin)

def gameloop(window, horloge):

    gameOver = False
    gameState = GameState()
    land = landing.Landing()
    nextAngle = 0
    angle = 0
    w, h = GameConfig.lander.get_size()

    while not gameOver:
        nextAngle = 0
        horloge.tick(100)
        pos = (100, 100)
        window.fill(0)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                nextAngle = Move.TurnLeft
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                nextAngle = Move.TurnRight
            if event.type == pygame.QUIT:
                gameOver = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameOver = True
        angle += nextAngle
        land.landingEntities.draw(window)
        blitRotate(window, GameConfig.lander, pos, (w / 2, h / 2), angle)

        pygame.display.flip()


def main():
    pygame.init()
    horloge = pygame.time.Clock()
    window = pygame.display.set_mode((GameConfig.windowW, GameConfig.windowH))
    pygame.display.set_caption("Planet Lander")

    gameloop(window, horloge)
    pygame.quit()
    quit()


# lancement de la fonction principale
main()
