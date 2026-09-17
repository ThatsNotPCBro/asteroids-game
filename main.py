import sys

import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import (
    ASTEROID_MIN_RADIUS,
    LARGE_ASTEROID_SCORE,
    MEDIUM_ASTEROID_SCORE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SMALL_ASTEROID_SCORE,
)
from logger import log_event, log_state
from player import Player
from shot import Shot


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    score_font = pygame.font.Font(None, 36)

    updatable: pygame.sprite.Group = pygame.sprite.Group()
    drawable: pygame.sprite.Group = pygame.sprite.Group()
    asteroids: pygame.sprite.Group = pygame.sprite.Group()
    shots: pygame.sprite.Group = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0.0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    if asteroid.radius <= ASTEROID_MIN_RADIUS:
                        player.add_score(SMALL_ASTEROID_SCORE)
                    elif asteroid.radius <= ASTEROID_MIN_RADIUS * 2:
                        player.add_score(MEDIUM_ASTEROID_SCORE)
                    else:
                        player.add_score(LARGE_ASTEROID_SCORE)
                    asteroid.split()

        screen.fill("black")

        score_text = score_font.render(f"Score: {player.score}", True, "white")
        screen.blit(score_text, (10, 10))

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
