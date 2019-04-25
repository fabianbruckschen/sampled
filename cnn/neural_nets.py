import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers.convolutional import Conv1D, MaxPooling1D


# tensorflow
# define univariate class
class TFUNET(Sequential):
    def __init__(self, n_features, n_filters,
                 n_timesteps, n_linear, n_outputs):
        super().__init__()
        self.add(Conv1D(filters=n_filters, kernel_size=3, activation='relu',
                        input_shape=(n_timesteps, n_features)))
        self.add(MaxPooling1D(pool_size=2))
        self.add(Flatten())
        self.add(Dense(n_linear, activation='relu'))
        self.add(Dense(n_outputs))


# define multivariate class
class TFMNET(Sequential):
    def __init__(self, n_features, n_filters,
                 n_timesteps, n_linear, n_outputs):
        super().__init__()
        self.add(Conv1D(filters=n_filters*2, kernel_size=3, activation='relu',
                        input_shape=(n_timesteps, n_features)))
        if n_timesteps >= 14:
            self.add(Conv1D(filters=n_filters*2, kernel_size=3,
                            activation='relu'))
            self.add(MaxPooling1D(pool_size=2))
        self.add(Conv1D(filters=n_filters, kernel_size=3, activation='relu'))
        self.add(MaxPooling1D(pool_size=2))
        self.add(Flatten())
        self.add(Dense(n_linear*10, activation='relu'))
        self.add(Dense(n_outputs))


# pytorcj
# define univariate class
class PTUNET(nn.Module):
    def __init__(self, n_features, n_filters,
                 n_timesteps, n_linear, n_outputs):
        super().__init__()
        self.n_filters = n_filters
        self.conv1 = nn.Conv1d(n_features, n_filters, 3, stride=1)
        self.aps = int(np.floor((n_timesteps-3+1)/2))
        self.l1 = nn.Linear(n_filters*self.aps, n_linear)
        self.l2 = nn.Linear(n_linear, n_outputs)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool1d(x, kernel_size=2)
        x = x.view(-1, self.n_filters*self.aps)  # flatten
        x = F.relu(self.l1(x))
        x = self.l2(x)
        return x


# define multivariate class
class PTMNET(nn.Module):
    def __init__(self, n_features, n_filters,
                 n_timesteps, n_linear, n_outputs):
        super().__init__()
        self.n_filters = n_filters
        self.n_timesteps = n_timesteps
        self.conv1 = nn.Conv1d(n_features, n_filters*2, 3, stride=1)
        self.conv2 = nn.Conv1d(n_filters*2, n_filters*2, 3, stride=1)
        self.conv3 = nn.Conv1d(n_filters*2, n_filters, 3, stride=1)
        self.aps = int(np.floor((n_timesteps-3+1)/4))
        self.l1 = nn.Linear(n_filters, n_linear*10)
        self.l2 = nn.Linear(n_linear*10, n_outputs)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        if self.n_timesteps >= 14:
            x = F.relu(self.conv2(x))
            x = F.max_pool1d(x, kernel_size=2)
        x = F.relu(self.conv3(x))
        x = F.max_pool1d(x, kernel_size=2)
        x = x.view(-1, self.n_filters)  # flatten
        x = F.relu(self.l1(x))
        x = self.l2(x)
        return x
