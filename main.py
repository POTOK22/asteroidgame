import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from live import Live


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroid Game")
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shot = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable, shot)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Live.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    dt = 0
    score = 0

    lives = [
        Live(SCREEN_WIDTH // 6 - 150, SCREEN_HEIGHT // 16),
        Live(SCREEN_WIDTH // 6 - 75, SCREEN_HEIGHT // 16),
        Live(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 16),
    ]

    font = pygame.font.Font(None, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        updatable.update(dt)

        for object_asteroid in asteroids:
            if player.collide(object_asteroid):
                player.reset_position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                object_asteroid.kill()
                if lives:
                    life = lives.pop()
                    life.kill()
                if not lives:
                    print("Game Over")
                    exit()

        for object_asteroid in asteroids:
            for object_shot in shot:
                if object_asteroid.collide(object_shot):
                    object_asteroid.split()
                    object_shot.kill()
                    score += object_asteroid.scoring(object_asteroid.radius)

        screen.fill((0, 0, 0))

        text_surface = font.render(str(score), True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(SCREEN_WIDTH // 1.1, SCREEN_HEIGHT // 16)
        )

        screen.blit(text_surface, text_rect)

        for object in drawable:
            object.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
