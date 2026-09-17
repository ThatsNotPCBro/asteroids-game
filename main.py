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
    game_over_font = pygame.font.Font(None, 72)

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
    game_over = False

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if not game_over:
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    game_over = True
                    break

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

        if game_over:
            game_over_text = game_over_font.render("GAME OVER", True, "white")
            game_over_rect = game_over_text.get_rect(center=screen.get_rect().center)
            screen.blit(game_over_text, game_over_rect)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
