# chargement des modules externes
import pygame
from GameConfig import GameConfig
from landing import Landing
from lander import Lander


class Move:
    Up = 5
    Down = -5
    TurnLeft = -2
    TurnRight = 2




def gameloop(window, horloge):
    gameOver = False
    land = Landing()
    aircraft = Lander()
    aircraft_team = pygame.sprite.Group()
    aircraft_team.add(aircraft)

    while not gameOver:
        horloge.tick(60)

        window.fill(0)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameOver = True
        if keys[pygame.K_LEFT]:
            aircraft.rotate(Move.TurnLeft)
        elif keys[pygame.K_RIGHT]:
            aircraft.rotate(Move.TurnRight)
        elif keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            aircraft.boost()

        land.landingEntities.update()
        land.landingEntities.draw(window)
        aircraft_team.update()
        aircraft_team.draw(window)
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
