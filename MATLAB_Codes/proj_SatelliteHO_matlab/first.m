clc;clear;close all;
%%
% Read the data from the .txt file (JDI) Just Do It
fileID = fopen('list_data/list_data_JDI.txt', 'r');
data = textscan(fileID, '%s', 'Delimiter', '\n');
data = data{1};
fclose(fileID);

% Process the data
for i = 1:numel(data)
    if contains(data{i}, '(')
        % Extract the numbers within parentheses
        numbers = sscanf(data{i}, '(%d, %d),');
        % Convert the numbers to cell arrays
        numbersCell = num2cell(reshape(numbers, 2, {}).', 2);
        % Replace parentheses with curly braces
        data{i} = strrep(data{i}, '(', '[');
        data{i} = strrep(data{i}, ')', ']');
        % Replace comma-separated numbers with square brackets
        data{i} = strrep(data{i}, num2str(numbers), num2str(numbersCell));
    end
end

% Write the modified data to a new .txt file
fileID = fopen('modified_data_JDI.txt', 'w');
fprintf(fileID, '%s\n', data{:});
fclose(fileID);
clear fileID ans numbersCell numbers i;