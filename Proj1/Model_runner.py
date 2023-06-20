import gym
import os
import sys
from stable_baselines3  import DQN
from stable_baselines3  import PPO
from stable_baselines3  import A2C
from satelliteenv import *
env=SatelliteEnv()

def funcPPO():
  Log_path=os.path.join('PPOTrSys','LogsSystem')
  PPO_path=os.path.join('PPOTrSys','Saved_models_Solv_Sys')
  model = PPO.load(PPO_path,env=env)  # loading the model from Saved_models.zip
  return model 


def funcDQN():
  Log_path=os.path.join('DQNTrSys','LogsSystem')
  DQN_path=os.path.join('DQNTrSys','Saved_models_Solv_Sys')
  model = DQN.load(DQN_path,env=env)  # loading the model from Saved_models.zip
  return model 


def funcA2C():
  Log_path=os.path.join('A2CTrSys','LogsSystem')
  A2C_path=os.path.join('A2CTrSys','Saved_models_Solv_Sys')
  model = A2C.load(A2C_path,env=env)  # loading the model from Saved_models.zip
  return model 





def main():
    algorithm = input("Enter algorithm (PPO, A2C, DQN): ")
    if algorithm.upper() == "PPO":
        m=funcPPO()
        return m
    elif algorithm.upper() == "A2C":
        m=funcA2C()
        return m
    elif algorithm.upper() == "DQN":
        m=funcDQN()
        return m
    else:
        print("Invalid algorithm")
        sys.exit()


if __name__ == "__main__":
    # Set model
    model=main()
    # model
    env.render_mode='human'
    obs = env.reset()
    for i in range(15000):
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()
        # print(obs)
        if done:
            # with open("Rewards_PPO_runner.txt", "a") as file:
            #         file.write(str(reward)+',')
            obs = env.reset()
    env.close()
