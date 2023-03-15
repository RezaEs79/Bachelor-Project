import pygame
import math
import numpy as np
import satellite
from satellite import Satellite
from RSS import CalcRSS
#

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#


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


def main():
    run = True
    clock = pygame.time.Clock()
    file_to_delete = open("data.txt",'w')
    file_to_delete.close()
    f = open("data.txt", "a")
    file_to_delete = open("demofile2.txt",'w')
    file_to_delete.close()
    fd = open("demofile2.txt", "a")
    # f.write("3")
    # earth = Satellite(0, 100, GREEN)
    # earth.earth = True

    irid1 = Satellite(350, 12, RED, 0.015)
    irid2 = Satellite(300, 10, LEMON)
    irid3 = Satellite(380, 8, BLUE, 0.05)

    # satellites = [ irid1, irid2, irid3]
    satellites = [ irid3]

    fig, ax = plt.subplots()

    x = np.arange(0, 2*np.pi, 0.01)
    line, = ax.plot(x, np.sin(x))


    def animate(i):
        line.set_ydata(np.sin(x + i / 50))  # update the data.
        return line,



    ani = animation.FuncAnimation(
        fig, animate, interval=20, blit=True, save_count=50)

    # To save the animation, use e.g.


    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        rEarth=200
        pygame.draw.circle(WIN, YELLOW, (400, 400), rEarth)
        for satellite in satellites:
            dist=math.sqrt(rEarth**2+satellite.r**2-2*satellite.r*rEarth*math.cos(math.pi/2-satellite.theta))
            # sigR=CalcRSS(dist)
            f.write(str(dist)+"   ")
            # fd.write(str(sigR)+"   ")
            # CalcRSS(dist,satellite.vel)
            satellite.update_position()
            satellite.draw(WIN)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()





