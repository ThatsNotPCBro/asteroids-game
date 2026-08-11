from circleshape import CircleShape
from constants import LINE_WIDTH, SHOT_RADIUS
import pygame

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def collides_with(self, other: "Shot") -> bool:
            return bool(self.position.distance_to(other.position) < self.radius + other.radius)