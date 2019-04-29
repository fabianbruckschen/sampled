import torch  # to tensor transformations
import numpy as np  # handling vectors and matrices
from torch.utils.data import TensorDataset, DataLoader  # pytorch training
import torch.nn.functional as F  # loss functions
from keras.optimizers import Adam  # tensorflow optimizer
from evaluation_functions import evaluate_forecasts


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
