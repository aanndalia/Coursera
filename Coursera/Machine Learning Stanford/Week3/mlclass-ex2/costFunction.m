function [J, grad] = costFunction(theta, X, y)
%COSTFUNCTION Compute cost and gradient for logistic regression
%   J = COSTFUNCTION(theta, X, y) computes the cost of using theta as the
%   parameter for logistic regression and the gradient of the cost
%   w.r.t. to the parameters.

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta
%
% Note: grad should have the same dimensions as theta
%

sum_term = 0;
j_sum_term = 0;
params = length(theta);
size(theta)
%size(grad)
%grad

for j = 1:params
	sum_term = 0;
	for i = 1:m
		xi = X(i,:);
		yi = y(i,1);
		sum_term = sum_term + (( (1 ./ (1 + e.^(-1 .* (theta' * xi')))) - yi)*xi(j));
	end
	grad(j) = (1/m) * sum_term;
end

for k = 1:m
	xk = X(k,:); % 1x3
	yk = y(k,1); % 1x1
	j_sum_term = j_sum_term + (-yk * log((1 ./ (1 + e.^(-1 .* (theta' * xk'))))) - (1-yk)*(log(1 - (1 ./ (1 + e.^(-1 .* (theta' * xk')))))));
end

J = (1/m) * j_sum_term


% =============================================================

end
