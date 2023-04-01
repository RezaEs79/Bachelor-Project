import pygame
from pygame import gfxdraw
import math
from math import pi
import random
from satellite import WIDTH, HEIGHT
RED = (188, 39, 50)

class User:
    Existing_users = []
    def __init__(self,radious_of_erth):
        self.connected_bs = []
        User.Existing_users.append(self)
        self.alpha=random.uniform(0, 2)
        self.x_u=int(WIDTH / 2 + round(radious_of_erth*math.cos(self.alpha*pi)))
        self.y_u=int(HEIGHT / 2 - round(radious_of_erth*math.sin(self.alpha*pi)))
        self.connect_id=0

    def connect_to_provider(self, providers):
        insight=[]
        for pr in providers:
            if self.alpha >= pr.footprint[0] and self.alpha <= pr.footprint[1]:
                insight.append(pr.id)
        if insight:
            self.connect_id= insight[0]
        else:
            self.connect_id=0
        insight.clear()
                
    def draw(self, win):
        for user in User.Existing_users:
            pygame.draw.circle(win, RED, (user.x_u, user.y_u), 3)



