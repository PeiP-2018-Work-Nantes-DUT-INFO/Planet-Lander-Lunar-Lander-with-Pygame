# chargement des modules externes
import pygame

from game_config import GameConfig
from components.landing import Landing
from components.lander import Lander
from os import path


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
    font = pygame.font.Font(path.join('Ressources', 'Bender_Light.otf'), GameConfig.FONTSIZE_HUD)
    offset = 0

    for i in [('SCORE : {0:04d}', score), ('FUEL : {0:03d}', lander.fuel)]:
        img = font.render(i[0].format(i[1]), True, GameConfig.WHITE)
        display_rect = img.get_rect()
        display_rect.topleft = (GameConfig.HUDLEFT_TOP_LEFT[0], GameConfig.HUDLEFT_TOP_LEFT[1] + offset)
        window.blit(img, display_rect)
        offset += GameConfig.FONTSIZE_HUD
    offset = 0
    for i in [('ALTITUDE : {0:04.0f}', GameConfig.WINDOW_H - lander.y), ('HORIZONTAL SPEED: {0:.0f}', lander.vx,),
              ('VERTICAL SPEED: {0:.0f}', lander.vy)]:
        img = font.render(i[0].format(i[1]), True, GameConfig.WHITE)
        display_rect = img.get_rect()
        display_rect.topleft = (GameConfig.HUD_RIGHT_TOPLEFT[0], GameConfig.HUD_RIGHT_TOPLEFT[1] + offset)
        window.blit(img, display_rect)
        offset += GameConfig.FONTSIZE_HUD


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

        window.fill(GameConfig.BACKGROUND_COLOR)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
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
        if aircraft.landed:
            if not aircraft.landed_in_grace:
                aircraft.explode(window)
                # render_center_text(surface, screen, "Kaboom! Your craft is destroyed.", (255,0,0))

        drawHUD(window, aircraft, 0)
        pygame.display.flip()

''' function main
    Usage : 
        - Fonction principale du jeux 
'''
def main():
    pygame.init()
    horloge = pygame.time.Clock()
    window = pygame.display.set_mode((GameConfig.WINDOW_W, GameConfig.WINDOW_H))
    pygame.display.set_caption("Planet Lander")

    gameloop(window, horloge)
    pygame.quit()
    quit()


# lancement de la fonction principale
main()
