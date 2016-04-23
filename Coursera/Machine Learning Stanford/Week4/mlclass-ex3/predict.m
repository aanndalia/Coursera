function p = predict(Theta1, Theta2, X)
%PREDICT Predict the label of an input given a trained neural network
%   p = PREDICT(Theta1, Theta2, X) outputs the predicted label of X given the
%   trained weights of a neural network (Theta1, Theta2)

% Useful values
m = size(X, 1);
num_labels = size(Theta2, 1);

% You need to return the following variables correctly 
p = zeros(size(X, 1), 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Complete the following code to make predictions using
%               your learned neural network. You should set p to a 
%               vector containing labels between 1 to num_labels.
%
% Hint: The max function might come in useful. In particular, the max
%       function can also return the index of the max element, for more
%       information see 'help max'. If your examples are in rows, then, you
%       can use max(A, [], 2) to obtain the max for each row.
%

m; % 5000
num_labels; % 10
size(p); % 5000x1
size(X); % 5000x400
size(Theta1); % 25x401
size(Theta2); % 10x26

col1 = ones(m,1); %5000x1

X1 = [col1 X]; % 5000x401

X2 = sigmoid(X1*Theta1'); % 5000x25

X2 = [col1 X2]; %5000x26

h = sigmoid(X2*Theta2'); %5000x10

for i=1:m
	[val, ind] = max(h(i,:), [], 2);
	p(i) = ind;
end

p


% =========================================================================


end
