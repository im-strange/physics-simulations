import pygame
import random
import math
import sys

pygame.init()
pygame.display.set_caption("projectile motion")
pygame.mouse.set_visible(False)

SCREEN_HEIGHT, SCREEN_WIDTH, FPS = 300, 800, 60
BG_COLOR, LINE_COLOR, ANGLE_COLOR = pygame.Color("grey12"), "orange", "orange"
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def random_color():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

def add_text(text, position, size, color):
    font_size = size
    font = pygame.font.Font(None, font_size)
    font.set_italic(True)
    font.set_bold(False)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

class Ball:
    def __init__(self, gravity, angle, power):
        self.color = random_color()
        self.path_color = "#3e3636"
        self.path_radius = 2
        self.radius = 15
        self.angle = angle
        self.power = power
        self.x = self.radius
        self.y = SCREEN_HEIGHT - self.radius
        self.gravity = gravity * 15
        self.mass = 10
        self.vx = math.cos(self.angle) * self.power
        self.vy = -math.sin(self.angle) * self.power
        self.time = 1 / FPS
        self.x_damping = 0.97
        self.y_damping = 0.9
        self.is_moving = True
        self.paths = []

    def draw(self):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.radius)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius - 3)

        if self.is_moving:
            self.paths.append((self.x, self.y))

    def add_gravity(self):
        self.vy += self.gravity * self.time
        self.y += (self.vy * self.time) + (0.5 * self.gravity * (self.time**2))

    def add_horizontal_velocity(self):
        self.x += self.vx * self.time
        if abs(self.vx) <= 0.7:
            self.is_moving = False

    def add_path(self):
        num = 0
        for points in self.paths:
            if num == 0:
                pygame.draw.circle(screen, self.path_color, points, self.path_radius)
                num = 1
            num -= 1
        if self.is_moving == False:
            self.paths.clear()

    def add_text(self):
        add_text(f"{round(math.degrees(self.angle))}°",
                 (self.x - self.radius / 2, self.y - self.radius / 4), 15, "black")

    def handle_wall_collision(self):
        if self.y >= SCREEN_HEIGHT - self.radius:
            self.y = SCREEN_HEIGHT - self.radius
            self.vy *= -self.y_damping
            self.vx *= self.x_damping
        if self.y <= self.radius:
            self.vy *= -1
        if self.x >= SCREEN_WIDTH - self.radius:
            self.vx *= -1
        if self.x <= self.radius:
            self.vx *= -1

def get_mouse_angle(mouse_x, mouse_y):
    x_comp = mouse_x
    y_comp = SCREEN_HEIGHT - mouse_y
    angle = math.atan2(y_comp, x_comp)
    return angle

def display_angle_line(mouse_x, mouse_y):
    length = 100
    angle = get_mouse_angle(mouse_x, mouse_y)
    end_x = math.cos(angle) * length
    end_y = SCREEN_HEIGHT - math.sin(angle) * length
    arc_radius = 30
    arc_rect = pygame.Rect(0 - arc_radius, SCREEN_HEIGHT - arc_radius, 2 * arc_radius, 2 * arc_radius)

    pygame.draw.line(screen, LINE_COLOR, (0, SCREEN_HEIGHT), (end_x, end_y), width=4)
    pygame.draw.arc(screen, ANGLE_COLOR, arc_rect, math.radians(270), angle, 2)

    round_angle = round(math.degrees(angle), 1)
    add_text(f"{round_angle}°", (40, SCREEN_HEIGHT - 20), 20, "white")

def draw_cursor(mouse_x, mouse_y):
    length = 10
    cursor_color = "white"
    pygame.draw.line(
        screen, cursor_color,
        (mouse_x - length, mouse_y),
        (mouse_x + length, mouse_y), width=1
    )
    pygame.draw.line(
        screen, cursor_color,
        (mouse_x, mouse_y - length),
        (mouse_x, mouse_y + length), width=1
    )

gravity = 9.8 * 10
power = 600
balls = []

while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_hypotenuse = math.sqrt((mouse_x)**2 + (SCREEN_HEIGHT - mouse_y)**2) * 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                angle = get_mouse_angle(mouse_x, mouse_y)
                ball = Ball(gravity, angle, power)
                balls.append(ball)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                balls.clear()

    screen.fill(BG_COLOR)

    for ball in balls:
        ball.add_path()

    for ball in balls:
        ball.draw()
        ball.add_text()
        ball.add_gravity()
        ball.add_horizontal_velocity()
        ball.handle_wall_collision()

    display_angle_line(mouse_x, mouse_y)
    draw_cursor(mouse_x, mouse_y)
    pygame.display.update()
    clock.tick(FPS)
    