function [C, sigma] = dataset3Params(X, y, Xval, yval)
%EX6PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = EX6PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
C = 1;
sigma = 0.3;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%

size(X); %211x2
size(y); %211x1
size(Xval); %200x2
size(yval); %200x1

x1 = Xval;
x2 = Xval;

examples_C = [0.01 0.03 0.1 0.3 1 3 10 30];
examples_sigma = [0.01 0.03 0.1 0.3 1 3 10 30];

error = zeros(length(examples_C));

for i = 1:length(examples_C)
	for j = 1:length(examples_sigma)
		model = svmTrain(X, y, examples_C(i), @(x1, x2) gaussianKernel(x1, x2, examples_sigma(j)));
		pred = svmPredict(model, Xval);
		error(i,j) = mean(double(pred ~= yval));
	end
end

[min_error, ind_error] = min(error(:));
[I,J] = ind2sub([size(error,1) size(error,2)], ind_error);

C = examples_C(I);
sigma = examples_sigma(J);

% =========================================================================

end
