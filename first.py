import pygame
import math
import numpy as np
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
GREEN = (0, 128, 0)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
PINK = (255, 128, 128)
PURPLE = (255, 0, 255)
INDIGO = (0, 0, 255)
LEMON = (0, 220, 128)
FONT = pygame.font.SysFont("comicsans", 16)


class Planet:
    # TIMESTEP = 3600*24  # 1 day
    TIMESTEP = 0.1  # 1 day

    def __init__(self, r, radius, color, vel=0.01):
        self.theta = -math.pi/2
        self.r = r
        self.x = self.r * math.sin(self.theta) + WIDTH / 2
        self.y = self.r * math.sin(self.theta) + HEIGHT / 2
        self.radius = radius
        self.color = color
        self.orbit = []
        self.earth = False
        self.distance_to_earth = 0

        self.vel = vel
        # distance_y = self.r*  math.sin(theta)
        # distance_x =self.r*  math.cos(theta)

        self.x_vel = self.vel * math.sin(self.theta)
        self.y_vel = self.vel * math.cos(self.theta)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

        if not self.earth:
            distance_text = FONT.render(
                f"{round((self.theta%(2*math.pi))/math.pi -1, 1)} \u03C0", 1, WHITE)
            win.blit(distance_text, (self.x - distance_text.get_width() /
                     2, self.y - distance_text.get_height()/2))

    def update_position(self):
        if not self.earth:
            self.distance_to_earth = math.sqrt(self.x**2+self.y**2)
            self.theta += self.vel * self.TIMESTEP
            self.x = WIDTH / 2 + self.r * math.cos(self.theta)
            self.y = WIDTH / 2 + self.r * math.sin(self.theta)
            self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    earth = Planet(0, 100, GREEN)
    earth.earth = True

    # irid1 = Planet(350, 12, RED)
    irid1 = Planet(350, 12, RED, 0.015)
    # irid1.y_vel = 24.077 * 1000
    irid2 = Planet(300, 10, LEMON)
    irid3 = Planet(380, 8, BLUE, 0.02)
    # mars.y_vel = 24.077 * 1000

    planets = [earth, irid1, irid2, irid3]
    # planets = [earth, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            pygame.draw.circle(WIN, YELLOW, (400, 400), 200)
            # for i in range (100):
            #     pass
                # pygame.draw.circle(WIN,RED, (400+i, 300+i), 1)
            planet.update_position()
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
