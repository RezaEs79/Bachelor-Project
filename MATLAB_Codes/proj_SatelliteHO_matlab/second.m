clc;clear;close all;
%%
% Define file paths
% filepaths = {'modified_data/modified_data_Train/modified_data_PPO.txt', ... 
%              'modified_data/modified_data_Train/modified_data_A2C.txt'};
filepaths = {'modified_data/modified_data_Train/modified_data_PPO.txt', ... 
             'modified_data/modified_data_Train/modified_data_A2C.txt', ...
             'modified_data/modified_data_JDI.txt'};         
% fileID = fopen('modified_data/modified_data_DQN.txt', 'r');
table=cell(1000,length(filepaths));
%%

% fileID = fopen(filepaths{1}, 'r');
% data = textscan(fileID, '%s', 'Delimiter', '\n');
% data = data{1};
% table(:,i)=data;

%%
% Read data from each file
for i = 1:length(filepaths)
%     data(i,:) = importdata(filepaths{i});
    fileID = fopen(filepaths{i}, 'r');
    data = textscan(fileID, '%s', 'Delimiter', '\n');
    data = data{1};
    table(:,i)=data;
end
clear fileID
%%
my_objects=cell(length(filepaths),size(data, 1));
for j = 1:length(filepaths)
    for i = 1:numel(data)
        str=table(i,j);
        splits = split(str, '**** ');
        value1 = str2double(splits{1});
        value2 = str2double(splits{2});
        value3 = str2double(splits{3});
        value4 = str2double(splits{4});
        cell_str = splits{5};
        % Define the input string

        % Replace parentheses with brackets and commas
        cell_str = strrep(cell_str, '(', '[');
        cell_str = strrep(cell_str, ')', ']');
        cell_str = strrep(cell_str, ', ', ',');
        % Evaluate the modified string
        value5 = eval(cell_str);
        mylist=Vec_to_Cell(value5);
        % Create a new object with the extracted values and add it to the list
        obj = MyClass(value1,value2,value3,value4,mylist);
        my_objects{j,i} = obj;
    end
end
clear data obj j i str listStr cell_str splits ...
    value1 value2 value3 value4 value5 mylist;
%%
mat=zeros(length(filepaths),7,size(my_objects,2));
for j=1:length(filepaths)
    for i = 1:size(my_objects,2)
         mat(j,1,i)=my_objects{j,i}.id;
         mat(j,2,i)=my_objects{j,i}.rss;
         mat(j,3,i)=my_objects{j,i}.capacity;
         mat(j,4,i)=my_objects{j,i}.height;
         mat(j,5,i)=Num_HO(my_objects{j,i}.memory);
         mat(j,6,i)=length(my_objects{j,i}.memory);
         mat(j,7,i)=find_single_change(my_objects{j,i}.memory);
    end
end
clear i j
%%
NUM_HO=zeros(length(filepaths),1);
for m=1:length(filepaths)
    NUM_HO(m,1)=sum(mat(m,5,:));
%     title(['iter ' num2str(m) ' Best= ' num2str(6)]);
end
%%
Vec_RSS=zeros(length(filepaths),1);
for m=1:length(filepaths)
    Vec_RSS(m,1)=sum(mat(m,2,:));
end
MagVec_RSS=abs(Vec_RSS);
min_val = min(MagVec_RSS);
max_val = max(MagVec_RSS);
if max_val > min_val
    dift_vec=max_val-MagVec_RSS;
    Vec_RSS=(dift_vec+max_val)/max_val;
end
%%
Vec_Capacity=zeros(length(filepaths),1);
for m=1:length(filepaths)
    Vec_Capacity(m,1)=sum(mat(m,3,:));
end
%%
Vec_Height=zeros(length(filepaths),1);
for m=1:length(filepaths)
    Vec_Height(m,1)=sum(mat(m,4,:));
end
%%
Vec_service_delivery=zeros(length(filepaths),1);
for m=1:length(filepaths)
    Vec_service_delivery(m,1)=sum(mat(m,6,:));
end
%%
HOPP=zeros(length(filepaths),1);
for m=1:length(filepaths)
    HOPP(m,1)=sum(mat(m,7,:));
end
%%
xlabels = {'PPO','A2C','JDI'};
colors = [
    1 0 0;
    0 1 0;
    0 0 1
];
%%
Vec_Total=[NUM_HO,Vec_RSS,Vec_Height,Vec_service_delivery,Vec_Capacity,HOPP];
figure(6);
X = categorical({'Num. HO','RSS','Height','Telecommunications Services','Capacity','HOPP'});
X = reordercats(X,{'Num. HO','RSS','Height','Telecommunications Services','Capacity','HOPP'});
Vec_Total(:,2:end-1) = Vec_Total(:,2:end-1)/10;
Vec_Total(:,3:end-1) = Vec_Total(:,3:end-1)/1000;
Vec_Total(:,end)=10-Vec_Total(:,end);
Vec_Total(:,3) = Vec_Total(:,3)/10;
Vec_Total(:,1) = Vec_Total(:,1)/40;
Vec_Total(:,4) = Vec_Total(:,4)*4;
Vec_Total(:,2) = Vec_Total(:,2)*40;
Vec_Total(:,:) = Vec_Total(:,:)*10;
b=bar(X,Vec_Total,'FaceColor','flat');
b(1).CData(5,:) = colors(1,:);
for c=1:length(filepaths)
    for g=1:length(X)
        b(c).CData(g,:) = colors(c,:);
    end
end
ylabel('% Performance Evaluation');
title('Comparing All Parameter for Different Models');
legend('PPO','A2C','Opt. Tel. Service','Location','Northwest')
%%
figure(1);
b=bar(NUM_HO,'FaceColor','flat');
for c=1:length(filepaths)
    b.CData(c,:) = colors(c,:);
end
set(gca, 'XTickLabel', xlabels);xlabel('Models');ylabel('Number of HO');
title('Comparing the number of Handover for different models');
clear i j c b m filepaths NUM_HO table min_val max_val
%% 
figure(2);
b=bar(Vec_RSS,'FaceColor','flat');
for c=1:2
    b.CData(c,:) = colors(c,:);
end
set(gca, 'XTickLabel', xlabels);xlabel('Models');ylabel('Connection RSS');
title('Comparing the Connection RSS for different models');
clear i j c b m filepaths NUM_HO table my_objects 
%%
figure(3);
b=bar(Vec_Height,'FaceColor','flat');
for c=1:length(filepaths)
    b.CData(c,:) = colors(c,:);
end
set(gca, 'XTickLabel', xlabels);xlabel('Models');ylabel('Connection Height');
title('Comparing the Connection Height for different models');
clear i j c b m filepaths NUM_HO table my_objects Vec_RSS Vec_Height
%%
figure(4);
b=bar(Vec_service_delivery,'FaceColor','flat');
for c=1:length(filepaths)
    b.CData(c,:) = colors(c,:);
end
set(gca, 'XTickLabel', xlabels);xlabel('Models');ylabel('Telecommunication service volume');
title('Comparing the Service Volume for different models');
clear i j c b m filepaths NUM_HO table my_objects Vec_RSS Vec_Height Vec_service_delivery
%%
figure(5);
b=bar(Vec_Capacity,'FaceColor','flat');
for c=1:length(filepaths)
    b.CData(c,:) = colors(c,:);
end
set(gca, 'XTickLabel', xlabels);xlabel('Models');ylabel('Telecommunication Free Capacity');
title('Comparing the Improvement Capacity for different models');
clear i j c b m filepaths NUM_HO table my_objects Vec_RSS Vec_Height Vec_service_delivery
%% time index (part a)
function tot_num = Num_HO(data)
    % Initialize the counter
    changeCount=0;
    % Iterate through the elements starting from the second one
    for i = 2:numel(data)
        % Compare the second element of the pair
        if ~isequal(data{i}, data{i-1})
            changeCount = changeCount + 1;
        end
    end
    tot_num=changeCount;
end

%% time index (part a)
function B = Vec_to_Cell(A)
    B = cell(size(A, 2)/2, 1);
    for i = 1:size(B, 1)
        B{i} = A(2*i-1: 2*i);
    end
end
%%
function num_changes = find_single_change(vec)
    changeCount=0;
    % Iterate through the elements starting from the second one
    for i = 2:numel(vec)-1
        % Compare the second element of the pair
        if ~isequal(vec{i}, vec{i-1}) && ~isequal(vec{i}, vec{i+1})
            changeCount = changeCount + 1;
        end
    end
    num_changes=changeCount;
end
