import torch  # to tensor transformations
import numpy as np  # handling vectors and matrices
from math import sqrt  # mathematical operations
from sklearn.metrics import mean_squared_error  # error metrics
from torch.utils.data import TensorDataset, DataLoader  # pytorch training
import torch.nn.functional as F  # loss functions
from keras.optimizers import Adam  # tensorflow optimizer


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


# daily persistence model
def daily_persistence(data):
    # get the total active power for the last day
    value = data[-1, 0]
    # return 7 day forecast
    return [value for _ in range(7)]


# weekly persistence model
def weekly_persistence(data, n_days=7):
    # return last n_days
    return data[-n_days:]

# week one year ago persistence model
def yearly_persistence(data):
	# get the data for the prior week
	return data[:, 0]

# tensorflow modeling
def train_tf_model(train_X, train_y, model,
                   batch_size, epochs, lr):
    # add optimizer and loss function
    model.compile(loss='mse', optimizer=Adam(lr=lr))

    # fit the model
    model.fit(train_X, train_y,
              epochs, batch_size, verbose=0)

    # return model and optimzer
    return model, model.optimizer


def pred_tf_model(test_X, test_y, model):
    # create predictions
    preds = model.predict(test_X)

    # print RMSE
    rmse = evaluate_forecasts(test_y, preds)
    print('Overall RMSE for TF model: %s!' % rmse[0])

    # return predictions and RMSE
    return preds, rmse


# pytorch modeling
def train_pt_model(train_X, train_y, model,
                   batch_size, epochs, lr):

    # transform data to tensors (reshape dimensions of X)
    train_X = torch.from_numpy(np.array(train_X.reshape(train_X.shape[0],
                                                        train_X.shape[2],
                                                        train_X.shape[1]),
                                        dtype='float32'))
    train_y = torch.from_numpy(np.array(train_y, dtype='float32'))

    # create dataloader
    train_Xy = DataLoader(TensorDataset(train_X, train_y),
                          batch_size,
                          shuffle=True)

    # build model
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = F.mse_loss

    # fit the model
    def fit(df, num_epochs, model, loss_fn, opt):
        for epoch in range(num_epochs):
            for xb, yb in df:
                # Generate predictions
                pred = model(xb)
                loss = loss_fn(pred, yb)
                # Perform gradient descent
                opt.zero_grad()
                loss.backward()
                opt.step()

    fit(train_Xy, epochs, model, loss_fn, opt)

    # return model and optimizer
    return model, opt


def pred_pt_model(test_X, test_y, model):

    # transform data to tensors (reshape dimensions of X)
    test_X = torch.from_numpy(np.array(test_X.reshape(test_X.shape[0],
                                                      test_X.shape[2],
                                                      test_X.shape[1]),
                              dtype='float32'))

    # create predictions
    preds = model(test_X).data.numpy()

    # print RMSE
    rmse = evaluate_forecasts(test_y, preds)
    print('Overall RMSE for PT model: %s!' % rmse[0])

    # return predictions and RMSE
    return preds, rmse
