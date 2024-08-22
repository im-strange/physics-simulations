import pygame
import math
import sys

pygame.init()
pygame.display.set_caption("inclined")

SCREEN_WIDTH, SCREEN_HEIGHT = 700, 400
BG_COLOR = "#3a3b3c"
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Inclined_Plane:
    def __init__(self):
        self.color = "white"
        self.angle = math.radians(30)
        self.start_x = SCREEN_WIDTH / 2
        self.start_y = SCREEN_HEIGHT
        self.length = SCREEN_WIDTH
        self.end_x = self.start_x + math.cos(self.angle) * self.length
        self.end_y = SCREEN_HEIGHT - math.sin(self.angle) * self.length

        print(self.length)

    def draw(self):
        pygame.draw.line(screen, self.color,
                         (self.start_x, self.start_y),
                         (self.end_x, self.end_y),
                         2)

class Object:
    def __init__(self):
        self.color = "orange"
        self.width = 30
        self.height = 30
        self.x = 0
        self.y = SCREEN_HEIGHT - self.height
        self.mass = 20

    def draw(self):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)

plane = Inclined_Plane()
box = Object()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)

    box.draw()
    plane.draw()
    pygame.display.update()