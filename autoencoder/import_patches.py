import numpy as np
import keras
from skimage import io


class ImportPatches(keras.utils.Sequence):

    def __init__(self, path_IDs, batch_size = 32, dim = (128, 128, 128), n_channels = 1,
                n_classes = 1, shuffle = True):

        self.dim = dim
        self.batch_size = batch_size
        self.path_IDs = path_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):

        return int(np.floor(len(self.path_IDs)) / self.batch_size)

    def __getitem__(self, index):

        indexes = self.indexes[index*self.batch_size:(index + 1)*self.batch_size]
        path_IDs_temp = [self.path_IDs[k] for k in indexes]

        X = self.__data_generation(path_IDs_temp)

        return X

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.path_IDs))

        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, path_IDs_temp):

        X = np.empty((self.batch_size, *self.dim, self.n_channels))

        for i, ID in enumerate(path_IDs_temp):
            ret = io.imread(ID)
            ret = ret.astype(np.float32)
            ch1 = np.reshape(ret[:,:,1], [np.size(ret[:,:,1], 1)])
            ch2 = np.reshape(ret[:,:,2], [np.size(ret[:,:,2], 2)])
            X[i, ] = (ch1, ch2)

        return X