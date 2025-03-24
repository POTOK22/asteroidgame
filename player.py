import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.vel = pygame.Vector2(0, 0)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * (self.radius / 1.5)
        a = self.position + forward * float(self.radius)
        b = self.position - forward * float(self.radius) - right
        c = self.position - forward * float(self.radius) + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Losing the velocity over time
        self.vel *= FRICTION
        self.position += self.vel * dt

        if not any(keys):
            if abs(self.vel.x) < 0.01:
                self.vel.x = 0
            if abs(self.vel.y) < 0.01:
                self.vel.y = 0

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        acceleration = forward * ACCELERATION_RATE * dt

        self.vel += acceleration

        self.vel *= FRICTION

        self.position += self.vel

    def reset_position(self, x, y):
        self.position = pygame.Vector2(x, y)

    def shoot(self):
        if self.timer > 0:
            return
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.timer = PLAYER_SHOOT_COOLDOWN
