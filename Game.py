# chargement des modules externes
import pygame

from GameConfig import GameConfig
from landing import Landing
from lander import Lander


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
    font = pygame.font.Font('Bender_Light.otf', GameConfig.fontSizeHud)
    offset = 0

    for i in [('SCORE : {0:04d}', score), ('FUEL : {0:03d}', lander.fuel)]:
        img = font.render(i[0].format(i[1]), True, GameConfig.white)
        display_rect = img.get_rect()
        display_rect.topleft = (GameConfig.hudLeftTopLeft[0], GameConfig.hudLeftTopLeft[1] + offset)
        window.blit(img, display_rect)
        offset += GameConfig.fontSizeHud
    offset = 0
    for i in [('ALTITUDE : {0:04.0f}', GameConfig.windowH - lander.y), ('HORIZONTAL SPEED: {0:.0f}', lander.vx,),
              ('VERTICAL SPEED: {0:.0f}', lander.vy)]:
        img = font.render(i[0].format(i[1]), True, GameConfig.white)
        display_rect = img.get_rect()
        display_rect.topleft = (GameConfig.hudRightTopRight[0], GameConfig.hudRightTopRight[1] + offset)
        window.blit(img, display_rect)
        offset += GameConfig.fontSizeHud


''' function gameloop
    Usage : 
        - fonction principale du jeux
    Arguments : 
        - window : fenêtre de jeux
        - horloge : variable permettant de gérer le taux de rafraichissement par seconde
'''
def gameloop(window, horloge):
    game_over = False
    land = Landing()
    aircraft = Lander()
    aircraft_team = pygame.sprite.Group()
    aircraft_team.add(aircraft)

    while not game_over:
        horloge.tick(60)

        window.fill(0)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                if event.key == pygame.K_UP:
                    print("BOOOST")
        if keys[pygame.K_LEFT]:
            aircraft.rotate(Move.turn_left)
        elif keys[pygame.K_RIGHT]:
            aircraft.rotate(Move.turn_right)
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            aircraft.boost()
        aircraft.check_collision(land.landingEntities)
        land.landingEntities.update()
        land.landingEntities.draw(window)
        aircraft_team.update()
        aircraft_team.draw(window)
        drawHUD(window, aircraft, 0)
        pygame.display.flip()

''' function main
    Usage : 
        - Fonction principale du jeux 
'''
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
