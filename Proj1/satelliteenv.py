from math import sqrt, cos, pi
import sys
from multipledispatch import dispatch
import pygame
import random
import numpy as np
import gym
from gym import spaces
from satellite import Satellite
from satellite import WIDTH, HEIGHT
from user import User
from RSS import CalcRSS

font=pygame.font.SysFont('Arial_bold',38)
# FONT = pygame.font.SysFont("comicsans", 16)
FPS = 60
Pale_Pink= (255, 228, 225)
Sky_Blue= (135, 206, 235)
Mustard_Yellow= (246, 214, 94)
Light_Gray=(211, 211, 211)
Light_Purple=(221, 160, 221)
Peach= (255, 218, 185)
Teal= (0, 128, 128)
Olive_Green=(128, 128, 0)
Navy_Blue=(0, 0, 128)
Coral= (255, 127, 80)
Lavender=(230, 230, 250)
Mint_Green= (152, 251, 152)
Dark_Red= (139, 0, 0)
Beige= (245, 245, 220)
Dark_Purple= (128, 0, 128)
colors=[Pale_Pink,Sky_Blue,Mustard_Yellow,Light_Gray,Light_Purple,Peach,Teal,Olive_Green,Navy_Blue,Coral,Lavender,Mint_Green,Dark_Red,Beige,Dark_Purple]
rEarth = 200
lensys=300
NOS=6 # Number of Sats
NOU=15 # Number of Sats
# mysd=64 # seed Train
mysd=17 # seed Test
Num_Opt_param = 4
def genrating_Usr(count):
    myli=[]
    for _ in range(count):
        myli.append(User(rEarth))
    return myli

def dist_Usr_Sat(myUser,id):
    distance = sqrt(Satellite.find_height_by_id(id)**2 + rEarth**2 - 2*Satellite.find_height_by_id(id)*rEarth*cos((Satellite.find_angle_by_id(id)-myUser.alpha)*pi))
    return distance

@dispatch()
def genrating_Sat():
    construct=[]
    A=Satellite(rEarth+80, 12, Pale_Pink, 0.015)
    B=Satellite(rEarth+50, 10, Mint_Green)
    C=Satellite(rEarth+100, 8, Sky_Blue, 0.05)
    D=Satellite(rEarth+90, 9, Dark_Red,0.07)
    E=Satellite(rEarth+60, 11, Navy_Blue, 0.09)
    F=Satellite(rEarth+70, 13, Peach,0.12)
    # construct.extend([A])
    construct.extend([A,B,C,D,E,F])
    return construct

@dispatch(int)
def genrating_Sat(NumSat):
    construct=[]
    np.random.seed(mysd)
    # Generate random numbers for each column
    col1 = np.random.uniform(300, 395, size=(NOS, 1))
    col2 = np.random.randint(9, 16, size=(NOS, 1))
    col3 = np.random.randint(0, 14, size=(NOS, 1))
    col4 = np.random.uniform(0.02, 0.1, size=(NOS, 1))
    # Concatenate columns to form the matrix
    matrix = np.hstack((col1, col2, col3, col4))
    for i in range(NumSat):
        # construct.append(Satellite(random.randint(300, 400),random.randint(9, 16),random_c,random.uniform(0.02, 0.1)))
        construct.append(Satellite(matrix[i][0],matrix[i][1], colors[int(matrix[i][2])],matrix[i][3]))
    return construct

class SatelliteEnv(gym.Env, Satellite, User):
    def __init__(self):
        User.__init__(self, 300)
        Satellite.__init__(self, rEarth+80,Pale_Pink, 0.015)
        # self.users = genrating_Usr(10)
        # User.Existing_users.pop(0)
        # self.sats = genrating_Sat()
        self.sats = genrating_Sat(NOS)
        Satellite.Satellites_constellation.pop(0)
        self.render_mode = None
        self.action_space = spaces.Discrete(NOS)
        # self.observation_space = spaces.Box(low=0, high=1, shape=(NOS, NOU, 4), dtype=np.float32)
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(NOS, Num_Opt_param), dtype=np.float32)
        self.system_len = lensys
        self.reward=0

    def step(self, action):
        for u in self.users:
            sight=u.connect_to_provider(self.sats)
            # print(sight)
            A = [[0 for _ in range(Num_Opt_param)] for _ in range(NOS)]
            if sight:
                all_parameter = [(t, dist_Usr_Sat(u,t), CalcRSS(dist_Usr_Sat(u,t)), Satellite.change_capacity_by_id(t)) for t in sight]
                if len(u.ULP) > 2:
                    Height_RSS_Const = [
                        [tup[1], tup[2],  tup[3], u.ULP[-1] == tup[0]] for tup in all_parameter]
                else:
                    Height_RSS_Const = [[tup[1], tup[2],  tup[3],  False] for tup in all_parameter]

                self.observation = Height_RSS_Const + A[len(Height_RSS_Const):]
                self.observation = np.array(self.observation)
                # print(self.observation[action])
                h = [item[1] for item in all_parameter]
                rss = [item[2] for item in all_parameter]
                capacity = [item[3] for item in all_parameter]
                if action<len(sight):
                    u.connect_id = sight[action]
                    u.dist.append(h[action])
                    u.abs_rss.append(rss[action])
                    u.capacity.append(capacity[action])
                    u.ULP.append(sight[action])
                    self.reward+=1
                    if self.observation[action][3] == 1:
                        self.reward += 1
                    if min(h) == h[action]:
                        self.reward += 1
                    if max(rss) == rss[action]:
                        self.reward += 1
                    if max(capacity) == capacity[action]:
                        self.reward += 1
                else:
                    self.reward-=1
                    u.connect_id = 0
            else:
                self.observation = A
                self.observation = np.array(self.observation)

        for satellite in self.sats:
            satellite.update_position()
            satellite.shadow(self.users)
            satellite.capacity=10        
            
        self.system_len -= 1
        if self.system_len <= 0:
            with open("Rewards_PPO.txt", "a") as file:
                    file.write(str(self.reward)+',')
            for u in self.users:
                # Save the list to a file
                with open("list_data.txt", "a") as file:
                    file.write(str(u.uid) + ' **** '+str(sum(u.abs_rss))+' **** ' +
                               str(sum(u.capacity))+' **** '+str(sum(u.dist))+' **** ' + str(u.ULP))
                    file.write('\n')         
            self.done = True
        else:
            self.done = False
        ## observation
        # for i in range(NOS):
        #     for j in range(NOU):
        #         self.observation[i][j] = [self.sats[i].theta, self.sats[i].capacity, self.users[j].alpha, self.done]
        # self.observation = np.array(self.observation)
        self.info = {}
        if self.render_mode == 'human':
            self.render()
        return self.observation, self.reward, self.done, self.info

    def reset(self):
        self.reward=0
        self.done = False
        self.users = genrating_Usr(NOU)
        User.Existing_users.pop(0)
        # self.observation = np.zeros((NOS, NOU, 4))
        # self.observation = np.array(self.observation)
        self.observation = [
            [0 for _ in range(Num_Opt_param)] for _ in range(NOS)]
        self.observation = np.array(self.observation)
        print("Reset ........")
        self.system_len=lensys

        if self.render_mode == 'human':
            pygame.init()
            pygame.display.set_caption('Satellite RL')
            self.display = pygame.display.set_mode((WIDTH, HEIGHT))
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont('Arial_bold', 380)
            self.render()

        return self.observation  # reward, done, info can't be included

    def render(self, render_mode='human'):
        
        # draw
        self.display.fill((150, 170, 160))
        pygame.draw.circle(self.display,(111, 78, 151), (400, 400), rEarth)
        # body
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for usr in self.users:
            usr.draw(self.display,self.users)
        for sat in self.sats:
            sat.draw(self.display)


        pygame.display.update()
        self.clock.tick(FPS)

    def close(self):
        pygame.quit()