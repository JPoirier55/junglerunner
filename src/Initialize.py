import pygame
import kezmenu
from pygame.locals import *
import pygame.font


from JungleRunner import Game

pygame.font.init()

class Menu(object):
    running = True
    def main(self, screen):
        clock = pygame.time.Clock()
        background = pygame.image.load('Images/intro.png')
        menu = kezmenu.KezMenu(
            ['Play!', lambda: Game().main(screen, 'map1.tmx', background)],
            ['Quit', lambda: setattr(self, 'running', False)],
        )
        menu.x = 275
        menu.y = 350
        menu.color = (83,47,32)
        menu.focus_color = (108,210,0)
        menu.font = pygame.font.SysFont("constantia", 50)
        menu.enableEffect('raise-col-padding-on-focus', enlarge_time=0.1)

        while self.running:
            menu.update(pygame.event.get(), clock.tick(30)/1000.)
            screen.blit(background, (0, 0))
            menu.draw(screen)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Menu().main(screen)

