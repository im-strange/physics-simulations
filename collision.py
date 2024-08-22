import pygame
import math
import sys

# start up
pygame.init()
pygame.display.set_caption("Collision")
pygame.mouse.set_visible(False)

# visuals
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 500
BG_COLOR = pygame.Color("grey12")
FPS = 70

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
click_sound = pygame.mixer.Sound('sounds/pop-sound.mp3')

def add_text(text, position, size, color):
    font_size = size
    font = pygame.font.Font(None, font_size)
    font.set_italic(True)
    font.set_bold(False)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

class Object:
    def __init__(self, x, vx, width, height, mass):
        self.color = "#dbae58"
        self.width = width
        self.height = height
        self.gravity = 9.8 ** 2
        self.mass = mass
        self.x = x
        self.y = SCREEN_HEIGHT - self.height
        self.vx = vx
        self.vy = 0
        self.time = 1 / FPS
        self.rect = self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.wall_collide = False
        self.wall_collision = 0

    def draw(self):
        self.rect = self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, self.rect)

        mass_text_color = BG_COLOR
        velocity_text_color = "white"

        mass_text = f"{self.mass}kg"
        vel_text = f"v = {round(self.vx, 2)}"

        add_text(mass_text,
                 (self.x + (self.width / 3) - len(mass_text) * 2, self.y + (self.height / 3)),
                 15, mass_text_color)

        add_text(vel_text,
                 (self.x, self.y - 15),
                 15, velocity_text_color)

        if self.vx > 0: self.xdir = 1
        if self.vx < 0: self.xdir = -1

        if self.wall_collide:
            click_sound.play()
            self.wall_collide = False

    def apply_gravity(self):
        self.vy += self.gravity * self.time
        self.y += (self.vy * self.time) + (0.5 * self.gravity * (self.time ** 2))

        self.x += self.vx * self.time

    def handle_wall_collision(self):
        if self.y >= SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
        if self.x >= SCREEN_WIDTH - self.width:
            self.vx *= -1
            self.wall_collide = True
            self.wall_collision += 1
        if self.x <= 0:
            self.vx *= -1
            self.wall_collide = True
            self.wall_collision += 1

    def show(self):
        self.draw()
        self.apply_gravity()
        self.handle_wall_collision()

def is_collision(object1, object2):
    distance = math.hypot(object1.x - object2.width - object2.x, object1.y - object2.y)
    return distance < object1.width + object2.width

def handle_collision(object1, object2):
    m1, m2 = object1.mass, object2.mass
    v1x, v2x = object1.vx, object2.vx

    new_v1x = (v1x * (m1 - m2) + 2 * m2 * v2x) / (m1 + m2)
    new_v2x = (v2x * (m2 - m1) + 2 * m1 * v1x) / (m1 + m2)

    object1.vx = new_v1x
    object2.vx = new_v2x

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

width1, height1 = 40, 40
object1 = Object(40, 0, width1, height1, 1)
object2 = Object(object1.x + width1 + 20, -30, 60, 60, 1000)

object_collisions = 0
wall_collisions = 0
total_collisions = 0
start_time = pygame.time.get_ticks()

# main loop
while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)

    object1.show()
    object2.show()
    draw_cursor(mouse_x, mouse_y)

    wall_collisions += object1.wall_collision + object2.wall_collision
    object1.wall_collision, object2.wall_collision = 0, 0
    total_collisions = wall_collisions + object_collisions

    if is_collision(object1, object2):
        handle_collision(object1, object2)
        click_sound.play()
        object_collisions += 1


    add_text(f"object_collisions: {object_collisions}", (10, 10), 15, "white")
    add_text(f"wall_collisions: {wall_collisions}", (10, 25), 15, "white")

    add_text(f"total_collisions: {total_collisions}", (10, 40), 15, "white")
    add_text(f"elapsed_time: {round(elapsed_time, 1)}s", (10, 55), 15, "white")

    pygame.display.update()
    clock.tick(FPS)
