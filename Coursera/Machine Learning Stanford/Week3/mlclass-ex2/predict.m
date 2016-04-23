function p = predict(theta, X)
%PREDICT Predict whether the label is 0 or 1 using learned logistic 
%regression parameters theta
%   p = PREDICT(theta, X) computes the predictions for X using a 
%   threshold at 0.5 (i.e., if sigmoid(theta'*x) >= 0.5, predict 1)

m = size(X, 1); % Number of training examples

% You need to return the following variables correctly
p = zeros(m, 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Complete the following code to make predictions using
%               your learned logistic regression parameters. 
%               You should set p to a vector of 0's and 1's
%

size(theta) % 3x1
size(X) % 100x3
size(p) %100x1

probs = X * theta;
s_probs = 1 ./ (1 + e.^(-1 .* probs));
p_length = length(p);

for i=1:p_length
	if s_probs(i) >= 0.5
		p(i) = 1;
	else
		p(i) = 0;
	end
end
	



% =========================================================================


end
