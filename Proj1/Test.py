from satelliteenv import SatelliteEnv
env = SatelliteEnv()
env.render_mode='human'
episodes = 50
# obs = env.reset()

for episode in range(episodes):
    done = False
    obs = env.reset()
    while not done:#not done:
        random_action = env.action_space.sample()
        # print("action",random_action)
        obs, reward, done, info = env.step(env.action_space.sample())
        # print('reward',reward)
        # print('obs: ',obs)


"""
In your case, you have 3 satellites and 10 users, so the observation space could include information such as:

- The current position and velocity of each satellite
- The current position and velocity of each user
- The signal strength between each satellite and user
- The data rate between each satellite and user
- The number of users currently connected to each satellite


Based on this information, you can define the observation space as a multi-dimensional array or tensor with appropriate dimensions for each variable. For example, if you have 3 satellites and 10 users, your observation space could be defined as follows:
self.observation_space = gym.spaces.Box(low=0, high=1, shape=(3, 10, 5), dtype=np.float32)

This creates an observation space with shape (3, 10, 5), where the first dimension represents the number of satellites (3), the second dimension represents the number of users (10), and the third dimension represents the different variables being observed (5). The variables being observed could be position (x,y,z), velocity (vx,vy,vz), signal strength, data rate, and number of connected users.

Note that this is just an example and you may need to adjust the shape and variables being observed based on your specific problem requirements.

"""
'''
import numpy as np

# create a tensor with shape (3, 10, 5)
tensor = np.zeros((3, 10, 5))

# fill the tensor with random values
for i in range(3):
    for j in range(10):
        for k in range(5):
            tensor[i][j][k] = np.random.rand()

print(tensor)
'''


