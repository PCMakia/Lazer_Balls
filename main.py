import pygame
from player import Player
from constants import *


def main():
    # Constructor
    pygame.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    Player_1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    #created Clock object
    time_control = pygame.time.Clock()
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        Player_1.update(dt)
        Player_1.draw(screen)

        # flip muxt be last
        pygame.display.flip()
        time_passed = time_control.tick(60)
        dt = time_passed/1000

if __name__ == "__main__":
    main()
