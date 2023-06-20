import os

# list of filenames to be removed
files_to_remove = ['Rewards_PPO.txt', 'list_data.txt', 'Rewards_JDI.txt','Rewards_Test_PPO.txt']

# directory path where files are located
directory_path = os.getcwd()

# loop through each file in the list
for file_name in files_to_remove:
    # construct the full path to the file
    file_path = os.path.join(directory_path, file_name)
    # check if the file exists
    if os.path.exists(file_path):
        # remove the file
        os.remove(file_path)
        print(f'Removed {file_name} from {directory_path}')
    else:
        print(f'{file_name} not found in {directory_path}')
