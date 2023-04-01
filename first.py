import pygame
from satellite import Satellite
from satellite import WIDTH, HEIGHT
from user import User
import numpy as np
import time

#
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill((67,78,75))
FPS=20
clock = pygame.time.Clock()
pygame.display.set_caption("Satellite Simulation")
font=pygame.font.SysFont('Arial_bold',38)
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
rEarth=200

def genrating_Usr(count):
    for _ in range(count):
        User(rEarth)

def genrating_Sat():
    Satellite(350, 12, PURPLE, 0.015)
    Satellite(300, 10, LEMON)
    Satellite(380, 8, BLUE, 0.05)



def main():
    genrating_Usr(10)
    genrating_Sat()
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(FPS)
        WIN.fill((67,78,75))
        pygame.draw.circle(WIN, YELLOW, (400, 400), rEarth)
        User.Existing_users[0].draw(WIN)
        for usr in User.Existing_users:
            usr.connect_to_provider(Satellite.Satellites_constellation)
            
        for satellite in Satellite.Satellites_constellation:
            satellite.update_position()
            satellite.shadow(User.Existing_users)
            satellite.draw(WIN)


        img=font.render(str(len(Satellite.Satellites_constellation)),True,(125,85,85))
        WIN.blit(img,img.get_rect(center=(400,400)).topleft)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()


