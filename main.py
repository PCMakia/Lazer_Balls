import asyncio

import pygame
from player import Player, Shot
from constants import *
from asteroid import Asteroid
from asteroidfield import AsteroidField


def clear_groups(*groups):
    for g in groups:
        g.empty()


async def main():
    pygame.init()
    pygame.font.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    target = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, target)
    AsteroidField.containers = (updatable,)
    Shot.containers = (projectiles, drawable, updatable)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    font_title = pygame.font.Font(None, 72)
    font_score = pygame.font.Font(None, 48)
    font_button = pygame.font.Font(None, 40)

    replay_rect = pygame.Rect(0, 0, 260, 64)
    replay_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

    while True:
        clear_groups(updatable, drawable, target, projectiles)
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        AsteroidField()
        kill_count = 0

        time_control = pygame.time.Clock()
        dt = 0

        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            screen.fill("black")

            updatable.update(dt)

            player_dead = False
            for obj in target:
                if obj.collide(player):
                    print("Game Over!")
                    player_dead = True
                    break
            if player_dead:
                playing = False
                break

            for obj in list(target):
                for bullet in list(projectiles):
                    if obj.collide(bullet):
                        obj.split()
                        bullet.kill()
                        kill_count += 1

            for obj in drawable:
                obj.draw(screen)

            pygame.display.flip()
            time_passed = time_control.tick(60)
            dt = time_passed / 1000
            await asyncio.sleep(0)

        waiting_replay = True
        while waiting_replay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if replay_rect.collidepoint(event.pos):
                        waiting_replay = False

            screen.fill("black")

            title = font_title.render("You died", True, "white")
            screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140)))

            score_surf = font_score.render(f"Kills: {kill_count}", True, "white")
            screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))

            pygame.draw.rect(screen, "gray", replay_rect, width=2)
            btn_label = font_button.render("Replay", True, "white")
            screen.blit(btn_label, btn_label.get_rect(center=replay_rect.center))

            pygame.display.flip()
            await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
