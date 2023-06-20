import numpy as np
import gym
from gym import spaces
import sys
from myfuncs import *
font = pygame.font.SysFont('Arial_bold', 38)
Num_act = NOS-1
Num_Opt_param = 4
class SpotbeamEnv(gym.Env, Satellite, User):
    def __init__(self):
        User.__init__(self)
        Satellite.__init__(self, 220, Lavender, vel=0.01)
        self.sats = genrating_Sat()
        Satellite.instances.pop(0)
        self.render_mode = None
        self.action_space = spaces.Discrete(NOS)
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(NOS, Num_Opt_param), dtype=np.float32)
        self.system_len = lensys
        self.reward = 0

    def step(self, action):
        for u in self.users:
            new_list = u.connect_to_provider(self.sats)
            A = [[0 for _ in range(Num_Opt_param)] for _ in range(NOS)]
            
            if new_list:
                all_parameter = [((t[0]), chord_length(Satellite.find_height_by_id(t[0][0]), u.distances(t[1])), CalcRSS(chord_length(
                    Satellite.find_height_by_id(t[0][0]), u.distances(t[1]))), Satellite.change_capacity_by_id(t[0][0])) for t in new_list]
                if len(u.ULP) > 2:
                    Height_RSS_Const = [
                        [tup[1], tup[2], tup[3],  u.ULP[-1] == tup[0]] for tup in all_parameter]
                else:
                    Height_RSS_Const = [[tup[1], tup[2], tup[3],  False]
                                        for tup in all_parameter]
                self.observation = Height_RSS_Const + A[len(Height_RSS_Const):]
                # print(self.observation[action])
                self.observation = np.array(self.observation)
                sight = [item[0] for item in all_parameter]
                h = [item[1] for item in all_parameter]
                rss = [item[2] for item in all_parameter]
                capacity = [item[3] for item in all_parameter]
                """
                max_index = rss.index(max(rss))
                u.connect_id = sight[max_index]
                u.dist.append(h[max_index])
                u.abs_rss.append(rss[max_index])
                u.capacity.append(capacity[max_index])
                u.ULP.append(sight[max_index])
                self.reward += 1
                if self.observation[max_index][3] == 1:
                    self.reward += 1
                if min(h) == h[max_index]:
                    self.reward += 1
                if max(rss) == rss[max_index]:
                    pass
                    # self.reward += 1
                if max(capacity) == capacity[max_index]:
                    self.reward += 1

                """
                # for Just Do It
                # u.connect_id = sight[0]; u.ULP.append(sight[0])
                # u.dist.append(h[0]); u.abs_rss.append(rss[0])
                # u.capacity.append(capacity[0])
                if action < len(sight):
                    u.connect_id = sight[action]
                    u.dist.append(h[action])
                    u.abs_rss.append(rss[action])
                    u.capacity.append(capacity[action])
                    u.ULP.append(sight[action])
                    self.reward += 1
                    if self.observation[action][3] == 1:
                        self.reward += 1
                    if min(h) == h[action]:
                        self.reward += 1
                    if max(rss) == rss[action]:
                        self.reward += 1
                    if max(capacity) == capacity[action]:
                        self.reward += 1
                else:
                    self.reward -= 1
                    u.connect_id = 0
                    # u.connect_id = sight[0]; u.ULP.append(sight[0])
                    # u.dist.append(h[0]); u.abs_rss.append(rss[0])

                
            else:
                self.observation = A
                self.observation = np.array(self.observation)

        for satellite in self.sats:
            satellite.update_position()
            satellite.shadow(self.users)
            satellite.capacity = 5  # Add this line for capacity
        self.system_len -= 1
        if self.system_len <= 0:
            print(f"total reward: {self.reward}")
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

        self.info = {}
        if self.render_mode == 'human':
            self.render()

        return self.observation, self.reward, self.done, self.info

    def reset(self):
        # Reset the environment
        self.reward = 0
        self.done = False
        self.users = genrating_Usr(NOU)
        # User.Existing_users.pop(0)
        # if len(User.Existing_users) > NOU+1:
        #     del User.Existing_users[:NOU]
        # else:
        #     User.Existing_users.pop(0)
        self.observation = [
            [0 for _ in range(Num_Opt_param)] for _ in range(NOS)]
        self.observation = np.array(self.observation)
        print("Reset ........")
        self.system_len = lensys
        if self.render_mode == 'human':
            pygame.init()
            pygame.display.set_caption('Spotbeam RL')
            self.display = pygame.display.set_mode((WIDTH, HEIGHT))
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont('Arial_bold', 380)
            self.render()

        return self.observation  # reward, done, info can't be included

    def render(self, render_mode='human'):

        # draw
        self.display.fill((130, 150, 140))
        pygame.draw.circle(self.display, Mint_Green, (WIDTH/2,
                           HEIGHT/2), side_dispersion_usr*sqrt(2), 1)
        # body
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for s in self.sats:
            s.draw(self.display)
        for usr in self.users:
            usr.draw(self.display,self.users)

        # User.draw(self.display)
        pygame.display.update()
        self.clock.tick(FPS)

    def close(self):
        pygame.quit()
