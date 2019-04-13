# import necessary modules
import pickle  # efficient file saving & loading


# reading and decoding binary pickles
def read_pickle(file_name):
    file = open(file_name, 'rb')
    data = pickle.load(file)
    return pickle.loads(data)
