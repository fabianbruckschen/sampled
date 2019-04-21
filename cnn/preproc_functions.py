import numpy as np  # handling vectors and matrices
from math import sqrt  # mathematical operations
from sklearn.metrics import mean_squared_error  # error metrics


# fill missing values with a value at the same time one day ago
def fill_missing(values):
    one_day = 60 * 24
    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            if np.isnan(values[row, col]):
                values[row, col] = values[row - one_day, col]


# split a univariate dataset into train/test sets by week
def split_dataset_by_weeks(data, trw, tew):
    # split into standard weeks
    train, test = data[trw[0]:trw[1]], data[tew[0]:tew[1]]
    # restructure into windows of weekly data
    train = np.array(np.split(train, len(train)/7))
    test = np.array(np.split(test, len(test)/7))
    return train, test

# create artificial weeks to enlarge dataset and map to corresponding y
def create_af_weeks(train, n_input, n_out, target_loc=0):
	# flatten data
	data = train.reshape((train.shape[0]*train.shape[1], train.shape[2]))
	X, y = list(), list()
	in_start = 0
	# step over the entire history one time step at a time
	for _ in range(len(data)):
		# define the end of the input sequence
		in_end = in_start + n_input
		out_end = in_end + n_out
		# ensure we have enough data for this instance
		if out_end < len(data):
			x_input = data[in_start:in_end, :]
			x_input = x_input.reshape((len(x_input), -1))
			X.append(x_input)
			y.append(data[in_end:out_end, target_loc])
		# move along one time step
		in_start += 1
	return np.array(X), np.array(y)

# evaluate one or more weekly forecasts against expected values
def evaluate_forecasts(actual, predicted):
    scores = list()
    # calculate an RMSE score for each day
    for i in range(actual.shape[1]):
        # calculate mse
        mse = mean_squared_error(actual[:, i], predicted[:, i])
        # calculate rmse
        rmse = sqrt(mse)
        # store
        scores.append(rmse)
    # calculate overall RMSE
    s = 0
    for row in range(actual.shape[0]):
        for col in range(actual.shape[1]):
            s += (actual[row, col] - predicted[row, col])**2
    score = sqrt(s / (actual.shape[0] * actual.shape[1]))
    return score, scores

# create new list out of 2 lists by combining every element
def list_combine(l1, l2):
    l = []
    for i in l1:
        for j in l2:
            l.append(i+j)
    return l