clc;clear;close all;
vec = [-2.6069 -1.3581 -7.0145 -0.1316 -7.0193 -0.8143 -0.8050 -4.1130 -1.2067 -0.8351 -0.8449 -6.9559];
min_val = min(vec);
max_val = max(vec);
if max_val > min_val
    vec = (vec - min_val) / (max_val - min_val);
end
%%
clc;clear;close all;
% Generate some sample data
x = 1:5;
y1 = [2 6 4 8 5];
y2 = [3 5 7 2 6];
y3 = [1 4 3 6 5];

% Create the figure and axes objects
figure;
ax = axes;

% Create the first two bar plots
bar(ax, x, y1);
hold on;
bar(ax, x, y2);

% Create the third bar plot with a light shadow
bar(ax, x, y3, 'FaceColor', 'interp', 'FaceAlpha', 0.5);

% Add labels and legend
xlabel('X');
ylabel('Y');
title('Bar Plot');
legend('Data 1', 'Data 2', 'Data 3 with Shadow');
%%
clc;clear;close all;
vec1 = [[1002, 3], [1002, 3], [1002, 3], [1002, 3],[1003, 5] ,[1002, 3], [1002, 3], [1002, 3], [1002, 3]] ;
num_changes1 = find_single_change(vec1); % num_changes1 will be 1

vec2 = [1002, 3, 1002, 3, 1002, 3, 1002, 3, 1003, 5, 1004, 3, 1004, 3, 1004, 3, 1004, 3];
num_changes2 =(diff(vec1)); % num_changes2 will be 1

function num_changes = find_single_change(vec)
% vec is a row vector
diff_vec = diff(vec);
num_changes = sum(diff_vec ~= 0);
end