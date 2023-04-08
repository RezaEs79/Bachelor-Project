import pygame
from pygame import gfxdraw
from math import pi,cos,sin
import random
from satellite import WIDTH, HEIGHT
from multipledispatch import dispatch
RED = (188, 39, 50)

class User:
    Existing_users = []
    def __init__(self,radious_of_erth,alpha):
        self.connected_bs = []
        User.Existing_users.append(self)
        self.alpha=alpha
        self.x_u=int(WIDTH / 2 + round(radious_of_erth*cos(self.alpha*pi)))
        self.y_u=int(HEIGHT / 2 - round(radious_of_erth*sin(self.alpha*pi)))
        self.connect_id=0
        self.ULP=[]


    @dispatch(list)
    def connect_to_provider(self, providers):
        insight=[]
        for pr in providers:
            if self.alpha >= pr.footprint[0] and self.alpha <= pr.footprint[1] or self.alpha >= pr.footprint[0]-2 and self.alpha <= pr.footprint[1]-2:
                insight.append(pr.id)
        
        if insight:
            # self.connect_id= insight[0]
            return insight

        else:
            self.connect_id=0
        return insight
    # @dispatch(list)
    # def connect_to_provider(self, providers):
    #     insight=[]
    #     for pr in providers:
    #         if self.alpha >= pr.footprint[0] and self.alpha <= pr.footprint[1] or self.alpha >= pr.footprint[0]-2 and self.alpha <= pr.footprint[1]-2:
    #             insight.append(pr.id)
        
    #     if insight:
    #         self.connect_id= insight[0]

    #     else:
    #         self.connect_id=0
    #     insight.clear()
    #     return 0
                
    @dispatch(pygame.Surface)
    def draw(self, win):
        for user in User.Existing_users:
            pygame.draw.circle(win, RED, (user.x_u, user.y_u), 3)
            
    @dispatch(pygame.Surface,list)
    def draw(self, win, usrlist):
        for user in usrlist:
            pygame.draw.circle(win, RED, (user.x_u, user.y_u), 3)



