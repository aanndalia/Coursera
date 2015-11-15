# read seaflow_data
seaflow_data <- read.csv(file="seaflow_21min.csv", head=TRUE, sep=",")
#seaflow_data <- read.csv(file="C:/Coursera/Introduction_to_Data_Science/seaflow_quiz/seaflow_21min.csv", head=TRUE, sep=",")

# Question 1
sum(seaflow_data["pop"] == "synecho")

# Question 2
summary(seaflow_data)

# Question 3
index <- 1:nrow(seaflow_data)
trainindex <- sample(index, trunc(nrow(seaflow_data) / 2))
trainset <- seaflow_data[trainindex, ]
testset <- seaflow_data[-trainindex, ]
mean_time <- colMeans(seaflow_data["time"])

# Question 4
pe <- seaflow_data$pe
chl_small <- seaflow_data$chl_small
pop <- seaflow_data$pop
qplot(pe, chl_small, colour=pop)

# Question 5, 6, 7
fol <- formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
model <- rpart(fol, method="class", data=trainset)
print(model)

# Question 8
predictions <- predict(model, newdata=testset, type="class")
sum(testset$pop == predictions) / length(predictions)

# Question 9
model_randomforest <- randomForest(fol, data=trainset)
predictions_randomforest <- predict(model_randomforest, newdata=testset, type="class")
sum(testset$pop == predictions_randomforest) / length(predictions_randomforest)

# Question 10
importance(model)

# Question 11
model_svm <- svm(fol, data=trainset)
predictions_svm <- predict(model_svm, newdata=testset, type="class")
sum(testset$pop == predictions_svm) / length(predictions_svm)

# Question 12
tree_table <- table(pred = predictions, true = testset$pop)
randomforest_table <- table(pred = predictions_randomforest, true = testset$pop)
svm_table <- table(pred = predictions_svm, true = testset$pop)

# Question 13
qplot(seaflow_data$fsc_perp, seaflow_data$fsc_big, colour=pop)

# Question 14
seaflow_data <- seaflow_data[seaflow_data$file_id != 208, ]
index <- 1:nrow(seaflow_data)
trainindex <- sample(index, trunc(nrow(seaflow_data) / 2))
trainset <- seaflow_data[trainindex, ]
testset <- seaflow_data[-trainindex, ]
fol <- formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
model_svm <- svm(fol, data=trainset)
predictions_svm <- predict(model_svm, newdata=testset, type="class")
sum(testset$pop == predictions_svm) / length(predictions_svm)

