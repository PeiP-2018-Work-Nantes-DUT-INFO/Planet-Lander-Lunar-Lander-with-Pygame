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


def drawHUD(window, lander, score):
    offset = 0
    for i in [('SCORE : {0:04d}', score), ('FUEL : {0:03d}', lander.fuel)]:
        font = pygame.font.Font(None, GameConfig.fontSizeHud)
        img = font.render(i[0].format(i[1]), True, GameConfig.white)
        display_rect = img.get_rect()
        display_rect.topleft = (GameConfig.hudLeftTopLeft[0], GameConfig.hudLeftTopLeft[1] + offset)
        window.blit(img, display_rect)
        offset += GameConfig.fontSizeHud
    offset = 0
    for i in [('ALTITUDE : {0:04.0f}', GameConfig.windowH - lander.y), ('HORIZONTAL SPEED: {0:.0f}', lander.vx,),
              ('VERTICAL SPEED: {0:.0f}', lander.vy)]:
        font = pygame.font.Font(None, GameConfig.fontSizeHud)
        img = font.render(i[0].format(i[1]), True, GameConfig.white)
        display_rect = img.get_rect()
        display_rect.topleft = (GameConfig.hudRightTopRight[0], GameConfig.hudRightTopRight[1] + offset)
        window.blit(img, display_rect)
        offset += GameConfig.fontSizeHud


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
                if event.key == pygame.K_UP:
                    print("BOOOST")
        if keys[pygame.K_LEFT]:
            aircraft.rotate(Move.TurnLeft)
        elif keys[pygame.K_RIGHT]:
            aircraft.rotate(Move.TurnRight)
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            aircraft.boost()

        land.landingEntities.update()
        land.landingEntities.draw(window)
        aircraft_team.update()
        aircraft_team.draw(window)
        drawHUD(window, aircraft, 0)
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
