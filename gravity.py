import pygame
import math
import sys

pygame.init()
pygame.display.set_caption("Gravity")

SCREEN_WIDTH, SCREEN_HEIGHT = 700, 500
BG_COLOR = pygame.Color("grey12")
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Ball:
    def __init__(self, x, y):
        self.color = "#dbae58"
        self.radius = 15
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.gravity = 9.8 ** 2
        self.time = 1 / FPS

    def draw(self):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.radius)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius - 3)

    def add_gravity(self):
        self.vy += self.gravity * self.time
        self.y += (self.vy * self.time) + (0.5 * self.gravity * (self.time ** 2))

    def handle_collision_wall(self):
        if self.y >= SCREEN_HEIGHT - self.radius:
            self.y = SCREEN_HEIGHT - self.radius

balls = []

while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                ball = Ball(mouse_x, mouse_y)
                balls.append(ball)

    screen.fill(BG_COLOR)

    for ball in balls:
        ball.draw()
        ball.add_gravity()
        ball.handle_collision_wall()

    pygame.display.update()
    clock.tick(FPS)