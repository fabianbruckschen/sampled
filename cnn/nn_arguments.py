# default values for training convolutional neural nets
class Arguments():
    def __init__(self):
        # net hyper parameters
        # general
        self.lr = 0.001
        self.n_filters = 16
        self.n_linear = 10
        # univariate specific
        self.epochs_u = 20
        self.batch_size_u = 4
        # multivariate specific
        self.epochs_m = 70
        self.batch_size_m = 16
        # dependent on data dimensions
        self.n_timesteps = 7
        self.n_features_u = 1
        self.n_features_m = 8
        self.n_outputs = 7
