function [theta, J_history] = gradientDescentMulti(X, y, theta, alpha, num_iters)
%GRADIENTDESCENTMULTI Performs gradient descent to learn theta
%   theta = GRADIENTDESCENTMULTI(x, y, theta, alpha, num_iters) updates theta by
%   taking num_iters gradient steps with learning rate alpha

% Initialize some useful values
m = length(y); % number of training examples
J_history = zeros(num_iters, 1);

for iter = 1:num_iters

    % ====================== YOUR CODE HERE ======================
    % Instructions: Perform a single gradient step on the parameter vector
    %               theta. 
    %
    % Hint: While debugging, it can be useful to print out the values
    %       of the cost function (computeCostMulti) and gradient here.
    %

	num_features = size(X,2);
	sum_vector = zeros(1,num_features);
	for i = 1:m
		xi = X(i,:);
		yi = y(i,1);
		real_term = ((xi*theta) - yi);
		vector_term = real_term * xi;
		sum_vector = sum_vector + vector_term;
	end

	delta = (1/m)*sum_vector;
	delta_transpose = delta';
	
	theta = theta - alpha * delta_transpose;









    % ============================================================

    % Save the cost J in every iteration    
    J_history(iter) = computeCostMulti(X, y, theta);

end

end
