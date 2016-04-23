function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

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

theta_sums = 0;
j_sum_term = 0;
sum_term = 0;

%size(theta)
%size(grad)
%theta

for k = 1:m
	xk = X(k,:); % 1x3
	yk = y(k,1); % 1x1
	j_sum_term = j_sum_term + (-yk * log((1 ./ (1 + e.^(-1 .* (theta' * xk'))))) - (1-yk)*(log(1 - (1 ./ (1 + e.^(-1 .* (theta' * xk')))))));
end

for r = 2:length(theta)
	theta_sums = theta_sums + (theta(r) .^ 2);
end

J = (1/m) * j_sum_term + (lambda / (2*m)) * theta_sums;
	
for j = 1:length(theta)
	sum_term = 0;
	for i = 1:m
		xi = X(i,:);
		yi = y(i,1);
		if j == 1
			sum_term = sum_term + (( (1 ./ (1 + e.^(-1 .* (theta' * xi')))) - yi)*xi(j));
		else
			sum_term = sum_term + (( (1 ./ (1 + e.^(-1 .* (theta' * xi')))) - yi)*xi(j)) + ((lambda / m) * theta(j));
		end
	end
	grad(j) = (1/m) * sum_term;
end

theta
grad
%disp("*************************************************")
%J
%grad
% =============================================================

end
