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
    title_font = pygame.font.Font(None, 72)
    prompt_font = pygame.font.Font(None, 36)

    updatable: pygame.sprite.Group = pygame.sprite.Group()
    drawable: pygame.sprite.Group = pygame.sprite.Group()
    asteroids: pygame.sprite.Group = pygame.sprite.Group()
    shots: pygame.sprite.Group = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable)

    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0.0
    game_state = "start_menu"

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if game_state in ("start_menu", "game_over"):
                    for sprite in list(updatable):
                        sprite.kill()
                    asteroid_field = AsteroidField()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    game_state = "playing"

        if game_state == "playing":
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    game_state = "game_over"
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

        if game_state == "start_menu":
            title_text = title_font.render("ASTEROIDS", True, "white")
            prompt_text = prompt_font.render("Start Game? Press ENTER", True, "white")
            screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH / 2, 280)))
            screen.blit(
                prompt_text, prompt_text.get_rect(center=(SCREEN_WIDTH / 2, 370))
            )
        else:
            score_text = score_font.render(f"Score: {player.score}", True, "white")
            screen.blit(score_text, (10, 10))

            for obj in drawable:
                obj.draw(screen)

            if game_state == "game_over":
                game_over_text = title_font.render("GAME OVER", True, "white")
                play_again_text = prompt_font.render("Play Again? Press ENTER", True, "white")
                screen.blit(
                    game_over_text,
                    game_over_text.get_rect(center=(SCREEN_WIDTH / 2, 280)),
                )
                screen.blit(
                    play_again_text,
                    play_again_text.get_rect(center=(SCREEN_WIDTH / 2, 370)),
                )

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
