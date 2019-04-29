import numpy as np  # handling vectors and matrices
from math import sqrt  # mathematical operations
from sklearn.metrics import mean_squared_error  # error metrics


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


# evaluate a naive pmp model
def evaluate_model(model_func, X, y):
    # walk-forward validation over each week
    predictions = []
    for i in range(len(X)):
        # predict the week
        yhat_sequence = model_func(X[i])
        # store the predictions
        predictions.append(yhat_sequence)
    predictions = np.array(predictions)
    # evaluate predictions days for each week
    score, scores = evaluate_forecasts(y, predictions)
    return score, scores, predictions


# summarize scores per naive model type
def summarize_scores(name, score, scores):
    s_scores = ', '.join(['%.1f' % s for s in scores])
    print('%s: [%.3f] %s' % (name, score, s_scores))
