clc;clear; close all;
% Define file paths
% filepaths = {'Rewards/Rewards_Train/Rewards_PPO.txt',...
%              'Rewards/Rewards_Train/Rewards_A2C.txt',...
%              'Rewards/Rewards_Train/Rewards_DQN.txt'};
% filepaths = {'Rewards/Rewards_Test/Rewards_RSS.txt',...
%              'Rewards/Rewards_Test/Rewards_A2C.txt',...
%              'Rewards/Rewards_Test/Rewards_DQN.txt'};
filepaths = {'Rewards/Rewards_Test/Rewards_A2C.txt',...
             'Rewards/Rewards_Test/Rewards_DQN.txt',...
             'Rewards/Rewards_Test/Rewards_RSS.txt'};
% Initialize data matrix
% data = zeros(length(filepaths), 500);
data = zeros(length(filepaths), 50);
% importdata(filepaths{1})

% Read data from each file
for i = 1:length(filepaths)
    data(i,:) = importdata(filepaths{i});
end
% Display the contents of the file (plot)
figure(1);
models=["A2C","DQN","RSS-Based"];
% models=["PPO","A2C"];
color=["g","b","m"];
sign=["-",":"];
%% ______________bar plot___________________________________
Y= zeros(1,length(filepaths));
for i = 1:length(filepaths)
    Y(i)=sum(data(i,:));
end
Y=(Y/max(Y))*100;
labels = Y;
X = categorical({'A2C','DQN', 'RSS-Based'});
X = reordercats(X,{'A2C','DQN', 'RSS-Based'});
hold on;
% Define colors for each bar
colors = ['g'; 'b'; 'm'];
% Plot each bar individually with the desired color
for i = 1:numel(X)
    bar(X(i), Y(i), 'FaceColor', colors(i));
    text(i, Y(i),"%"+ num2str(labels(i)), 'HorizontalAlignment', 'center', 'VerticalAlignment', 'cap');
end
title('Comparing Different Models');
xlabel('Model');ylabel('% Performance Evaluation');
hold off;
% ______________________________________________________
%%
for i = 1:length(filepaths)
%     plot(data(i,:),color(i),'linewidth',1.2);
    plot(data(i,:),sign(i)+color(i),'linewidth',5-i);
    %     legend(models(i));
    title('Rewards per Episode for each Model');
    xlabel('Episode');ylabel('Reward');
    hold on;
end
legend(models,'Location','SouthWest')
clear filepaths i color