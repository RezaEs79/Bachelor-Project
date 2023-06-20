from tensorboard.backend.event_processing import event_accumulator
Log_path='PPOTrSys\LogsSystem'
ea = event_accumulator.EventAccumulator(Log_path)
ea.Reload()

# Get the episode rewards
episode_rewards = ea.scalars.Items('Env/Reward')

# Extract the step and value for each reward
steps = [x.step for x in episode_rewards]
values = [x.value for x in episode_rewards]

# Plot the rewards using matplotlib
import matplotlib.pyplot as plt
plt.plot(steps, values)
plt.xlabel('Step')
plt.ylabel('Episode Reward')
plt.show()
# tensorboard --logdir .\PPOTrSys\LogsSystem\PPO_2\
