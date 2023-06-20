import os
import sys
from stable_baselines3 import PPO
from stable_baselines3 import DQN
from stable_baselines3 import A2C
from satelliteenv import *
timestep=150000
def funcPPO():
  Log_path=os.path.join('PPOTrSys','LogsSystem')
  PPO_path=os.path.join('PPOTrSys','Saved_models_Solv_Sys')

  env=SatelliteEnv()
  model=PPO('MlpPolicy',env,verbose=1,tensorboard_log=Log_path)
  # env.render_mode='human'
  # model.learn(total_timesteps=10)
  # env.close()
  env.render_mode=None
  # model.learn(total_timesteps=10000)
  model.learn(total_timesteps=timestep,tb_log_name="PPO")

  model.save(PPO_path)

def funcDQN():
  Log_path=os.path.join('DQNTrSys','LogsSystem')
  DQN_path=os.path.join('DQNTrSys','Saved_models_Solv_Sys')

  # Define the environment
  env=SatelliteEnv()
  # Define the model
  model = DQN('MlpPolicy', env, verbose=1,tensorboard_log=Log_path)
  # Train the model
  env.render_mode=None
  model.learn(total_timesteps=timestep)
  # save
  model.save(DQN_path)

def funcA2C():
  Log_path=os.path.join('A2CTrSys','LogsSystem')
  A2C_path=os.path.join('A2CTrSys','Saved_models_Solv_Sys')

  # Define the environment
  env=SatelliteEnv()
  # Define the model
  model = A2C('MlpPolicy', env, verbose=1,tensorboard_log=Log_path)
  # Train the model
  env.render_mode=None
  model.learn(total_timesteps=timestep)
  # save
  model.save(A2C_path)

def main():
    algorithm = input("Enter algorithm (PPO, A2C, DQN): ")

    if algorithm.upper() == "PPO":
        funcPPO()
    elif algorithm.upper() == "A2C":
        funcA2C()
    elif algorithm.upper() == "DQN":
        funcDQN()
    else:
        print("Invalid algorithm")
        sys.exit()


if __name__ == "__main__":
    main()

# model = PPO.load(PPO_path,env=env)  # loading the model from Saved_models.zip
# env.render_mode='human'
# obs = env.reset()
# for i in range(2000):
#     action, _state = model.predict(obs, deterministic=True)
#     obs, reward, done, info = env.step(action)
#     env.render()
#     print(reward)
#     if done:
#       obs = env.reset()
# env.close()