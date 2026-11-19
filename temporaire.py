
import pygame
import math

pygame.init()

# Configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mathematica - Le cristal")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 20)

# Couleurs
BLACK = (15, 18, 30)
WHITE = (240, 240, 240)
BLUE = (60, 150, 255)
GOLD = (255, 210, 70)
GREEN = (70, 220, 130)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def norm(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        n = self.norm()
        if n != 0:
            return Vector(self.x/n, self.y/n)
        return Vector(0, 0)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


class Entity:
    def __init__(self, x, y, radius, color):
        self.position = Vector(x, y)
        self.radius = radius
        self.color = color

    def draw(self):
        pygame.draw.circle(
            screen, self.color,
            (int(self.position.x), int(self.position.y)),
            self.radius
        )


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 16, BLUE)
        self.speed = 4

    def update(self, keys):
        direction = Vector(0, 0)

        if keys[pygame.K_z]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_q]:
            direction.x -= 1
        if keys[pygame.K_d]:
            direction.x += 1

        direction = direction.normalize()
        self.position = self.position + direction * self.speed

        self.position.x = max(16, min(WIDTH-16, self.position.x))
        self.position.y = max(16, min(HEIGHT-16, self.position.y))


class Crystal(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 22, GOLD)
        self.strength = 1.0

    def field(self, position):
        # Champ radial attractif
        direction = self.position - position
        distance = max(direction.norm(), 1)
        return direction.normalize() * self.strength


class Particle(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 7, GREEN)
        self.velocity = Vector(0, 0)

    def update(self, crystal):
        acceleration = crystal.field(self.position)
        self.velocity = self.velocity + acceleration * 0.04

        # Limitation de vitesse
        if self.velocity.norm() > 3:
            self.velocity = self.velocity.normalize() * 3

        self.position = self.position + self.velocity


class Game:
    def __init__(self):
        self.player = Player(100, 300)
        self.crystal = Crystal(400, 300)
        self.particle = Particle(200, 300)
        self.running = True
        self.won = False

        self.target = Vector(650, 300)

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        self.particle.update(self.crystal)

        distance = (
            self.particle.position - self.target
        ).norm()

        if distance < 20:
            self.won = True

    def draw(self):
        screen.fill(BLACK)

        # Réceptacle
        pygame.draw.circle(
            screen, GREEN,
            (int(self.target.x), int(self.target.y)), 20, 3
        )

        self.player.draw()
        self.crystal.draw()
        self.particle.draw()

        screen.blit(
            font.render("ZQSD : déplacement", True, WHITE),
            (20, 20)
        )

        if self.won:
            screen.blit(
                font.render("CRISTAL ACTIVE !", True, GOLD),
                (310, 500)
            )

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()
            self.draw()
            clock.tick(60)

        pygame.quit()


game = Game()
game.run()
