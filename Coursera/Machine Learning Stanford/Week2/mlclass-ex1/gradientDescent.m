function [theta, J_history] = gradientDescent(X, y, theta, alpha, num_iters)
%GRADIENTDESCENT Performs gradient descent to learn theta
%   theta = GRADIENTDESENT(X, y, theta, alpha, num_iters) updates theta by 
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
    %       of the cost function (computeCost) and gradient here.
    %
	
	theta0 = theta(1,1);
	theta1 = theta(2,1);
	sum_vector = zeros(1,2);
	for i = 1:m
		xi = X(i,2);
		yi = y(i,1);
		real_term = ((theta0 + theta1 * xi) - yi);
		vector_term = real_term * X(i, :);
		sum_vector = sum_vector + vector_term;
	end

	delta = (1/m)*sum_vector;
	delta_transpose = delta';
	
	theta = theta - alpha * delta_transpose;

    % ============================================================

    % Save the cost J in every iteration    
    J_history(iter) = computeCost(X, y, theta);

end

end
