import pygame
import math
from constants import *
from circleshape import CircleShape


class Live(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)

    def draw(self, screen):
        # pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        points = []
        for t in range(0, 360, 2):  # Loop through 0 to 360 degrees
            angle = math.radians(t)
            x = 16 * math.sin(angle) ** 3
            y = (
                13 * math.cos(angle)
                - 5 * math.cos(2 * angle)
                - 2 * math.cos(3 * angle)
                - math.cos(4 * angle)
            )

            # Scale and offset to position it on the screen
            px = self.position.x + int(x * 2)
            py = self.position.y - int(
                y * 2
            )  # Invert y to match Pygame's coordinate system
            points.append((px, py))

        pygame.draw.aalines(screen, "white", True, points, 2)  # Draw smooth heart shape

    def lose_live(self):
        self.kill()
