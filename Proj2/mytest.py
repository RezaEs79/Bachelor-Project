from spotbeamenv import *

myenv = SpotbeamEnv()
myenv.render_mode = 'human'
state = myenv.reset()

num_steps = 30000   # 9999 # 33 times
for s in range(num_steps):
    # sample a random action from the list of available actions
    action = myenv.action_space.sample()
    # action = 0
    # perform this action on the environment
    myenv.step(action)
    # print(myenv.observation)
    if myenv.done==True:
        with open("Rewards_JDI.txt", "a") as file:
                file.write(str(myenv.reward)+',')
        myenv.reset()

    # print the new state
    # myenv.render()

# end this instance of the taxi environment
myenv.close()
