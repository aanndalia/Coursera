function J = computeCost(X, y, theta)
%COMPUTECOST Compute cost for linear regression
%   J = COMPUTECOST(X, y, theta) computes the cost of using theta as the
%   parameter for linear regression to fit the data points in X and y

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta
%               You should set J to the cost.

sum = 0;
theta0 = theta(1,1);
theta1 = theta(2,1);
for i = 1:m
    xi = X(i,2);
	yi = y(i,1);
	sum = sum + ((theta0 + theta1 * xi) - yi)^2;
end

J = (1 / (2*m)) * sum;


% =========================================================================

end
