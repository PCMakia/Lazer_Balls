import pygame
from player import Player, Shot
from constants import *
from asteroid import Asteroid
from asteroidfield import AsteroidField


def main():
    # Constructor zone
    pygame.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
        # Creating group zone
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    target = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, target)
    AsteroidField.containers = (updatable)
    Shot.containers = (projectiles, drawable, updatable)

    # initialize zone
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    Player_1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    barrage = AsteroidField()

    #created Clock object
    time_control = pygame.time.Clock()
    dt = 0

    # Game loop zone
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        updatable.update(dt)
        for obj in target:
            if obj.collide(Player_1):
                print("Game Over!")
                exit(0)
        for obj in target:
            for bullet in projectiles:
                if obj.collide(bullet):
                    obj.split()
                    bullet.kill()
        for obj in drawable:
            obj.draw(screen)

        # these muxt be last
        pygame.display.flip()
        time_passed = time_control.tick(60)
        dt = time_passed/1000

if __name__ == "__main__":
    main()
