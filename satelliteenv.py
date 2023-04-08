import time
from multipledispatch import dispatch
import pygame
import random
import numpy as np
import gym
from gym import spaces
from satellite import Satellite
from satellite import WIDTH, HEIGHT
from user import User

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
def genrating_Usr(count):
    myli=[]
    for _ in range(count):
        myli.append(User(rEarth,random.uniform(0, 2)))
    return myli
@dispatch()
def genrating_Sat():
    construct=[]
    A=Satellite(350, 12, Pale_Pink, 0.015)
    B=Satellite(300, 10, Mint_Green)
    C=Satellite(380, 8, Sky_Blue, 0.05)
    # construct.extend([A])
    construct.extend([A,B,C])
    return construct
@dispatch(int)
def genrating_Sat(NumSat):
    construct=[]
    for i in range(NumSat):
        random_c = random.choice(colors)
        construct.append(Satellite(random.randint(300, 400),random.randint(6, 10),random_c,random.uniform(0.02, 0.1)))
    return construct


class SatelliteEnv(gym.Env, Satellite, User):
    def __init__(self):
        User.__init__(self, 300,0)
        Satellite.__init__(self, 220, 4,Lavender, vel=0.01)
        # self.users = genrating_Usr(10)
        # User.Existing_users.pop(0)
        self.sats = genrating_Sat()
        # self.sats = genrating_Sat(15)
        Satellite.Satellites_constellation.pop(0)
        self.render_mode = None
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0, high=1, shape=(3, 10, 4), dtype=np.float32)
        self.system_len = lensys

    def step(self, action):
        
        for u in self.users:
            sight=u.connect_to_provider(self.sats)
            if sight:
                if action<len(sight):
                    u.connect_id=sight[action]
                    u.ULP.append(sight[action])
                    self.reward+=1
                    if u.ULP[-1]==sight[action]:
                        self.reward+=10

                else:
                    self.reward-=2
                    u.connect_id=sight[0]
                    u.ULP.append(sight[0])



            

        for satellite in self.sats:
            satellite.update_position()
            satellite.shadow(self.users)        
            # if satellite.flag==1:
                # self.reward+=satellite.capacity
            
        self.system_len -= 1
        if self.system_len <= 0:
            # print(f"total reward: {self.reward}")
            
            done = True
        else:
            done = False


        # observation
        for i in range(3):
            for j in range(10):
                self.observation[i][j] = [self.sats[i].theta, self.sats[i].capacity, self.users[j].alpha, self.done]
        # self.observation = [self.orbit[0][0],self.orbit[0][1], self.x_u,self.y_u,action]
        self.observation = np.array(self.observation)
    
        # observation
        # self.observation = [self.Satellites_constellation[0].x,self.Satellites_constellation[0].x, self.x_u,self.y_u,action]
        # self.observation = np.array(self.observation)
    

        # B: eating apple
        # if self.prev_score < self.score:
        #     reward_b = 10
        #     self.prev_score = self.score
        #     self.timestep_passed_eating = 0
        #     self.valid_timestep_to_eat += 1
        # else:
        #     reward_b = 0
        #     self.timestep_passed_eating += 1

        # # D: punishment for wasting time
        # reward_d = -self.timestep_passed_eating // self.valid_timestep_to_eat
        # self.reward = reward_b  + reward_d

        self.info = {}

        if self.render_mode == 'human':
            self.render()

        return self.observation, self.reward, done, self.info

    def reset(self):
        self.done = False
        #'''
        self.users = genrating_Usr(10)
        User.Existing_users.pop(0)
        for u in self.users:
            print(f"{u.alpha:.2f}",end=" ")
        #'''
        self.observation = np.zeros((3, 10, 4))
        self.observation = np.array(self.observation)
        # self.observation = np.array(self.observation)
        print("Reset ........")
        self.system_len=lensys
        # reward
        self.reward = 0

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
        self.display.fill((98, 110, 104))
        pygame.draw.circle(self.display,(111, 78, 151), (400, 400), rEarth)
        # body
        for usr in self.users:
            usr.draw(self.display,self.users)
        for sat in self.sats:
            sat.draw(self.display)


        pygame.display.update()
        self.clock.tick(FPS)

    def close(self):
        pygame.quit()




myenv=SatelliteEnv()
myenv.render_mode='human'
state = myenv.reset()

num_steps = 999
for s in range(num_steps+1):
    # print(f&quotstep: {s} out of {num_steps}&quot)

    # sample a random action from the list of available actions
    action = myenv.action_space.sample()

    # perform this action on the environment
    myenv.step(action)

    # print the new state
    # myenv.render()

# end this instance of the taxi environment
myenv.close()
