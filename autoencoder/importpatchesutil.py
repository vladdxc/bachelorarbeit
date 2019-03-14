import numpy as np
import keras
from skimage import io
import h5py


class ImportPatches(keras.utils.Sequence):
    """"
    Class used to feed the data to the generator at training time, in order to avoid using up all the RAM.
    """
    def __init__(self, path_IDs, batch_size=32, dim=(128, 128, 128), n_channels=2,
                 n_classes=2, fmt='tif', norm_type='none', shuffle=True):
        'Initialization method'
        'Note that we do not need labels because we are working with autoencoders'
        self.dim = dim
        self.batch_size = batch_size
        self.path_IDs = path_IDs #a list of strings containing the names of the files to read data from,
                                # e.g. ['example_1.tif', example_2.tif', ...]
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.fmt = fmt #Format in which data is stored. Valid values are .mat and .tif
        self.norm_type = norm_type #Normalization type. Supported normalization types are 'max1', 'squash', 'standard'
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        'Number of batches per epoch'
        return int(np.floor(len(self.path_IDs)) / self.batch_size)

    def __getitem__(self, index):
        'Generate one batch of data'
        indexes = self.indexes[index*self.batch_size:(index + 1)*self.batch_size]
        path_IDs_temp = [self.path_IDs[k] for k in indexes]

        X = self.__data_generation(path_IDs_temp)

        return X

    def on_epoch_end(self):
        'Update and shuffle indexes at the end of each epoch'
        self.indexes = np.arange(len(self.path_IDs))

        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def normalize_input_data(self, arr):
        'Normalize input data.'

        norm_arr = np.empty((*self.dim, self.n_channels))
        supported_norm_types = ['standard', 'squash', 'max1']
        if self.norm_type not in supported_norm_types:
            norm_arr = arr

        elif self.norm_type == supported_norm_types[0]:
            for i in range(self.n_channels):
                tmp = arr[:, :, i]
                norm_arr[:, :, i] = np.divide(tmp - np.mean(tmp), np.std(tmp))
        elif self.norm_type == supported_norm_types[1]:
            for i in range(self.n_channels):
                tmp = arr[:, :, i]
                norm_sq = np.dot(tmp, tmp)
                squash_factor = np.sqrt(norm_sq)/(1 + norm_sq)
                norm_arr[:, :, i] = squash_factor*tmp
        elif self.norm_type == supported_norm_types[2]:
            for i in range(self.n_channels):
                tmp = arr[:, :, i]
                norm_arr[:, :, i] = tmp/np.amax(tmp)

        return norm_arr

    def __data_generation(self, path_IDs_temp):
        'Generate data, containing a number of samples equal to batch_size.'

        Xnn = np.empty((self.batch_size, *self.dim, self.n_channels))
        X = np.empty((self.batch_size, *self.dim, self.n_channels))
        valid_fomats = ['mat', 'tif']

        if self.fmt not in valid_fomats:
            raise ValueError('Please give correct format! Only .mat and .tif are supported')
        elif not isinstance(self.fmt, str):
            raise TypeError('Please type a string as format!')
        elif self.fmt == valid_fomats[0]:
            for i, ID in enumerate(path_IDs_temp):
                ret = io.imread(ID)
                ret = ret.astype(np.float32)
                X[i, ] = self.normalize_input_data(ret)
        elif self.fmt == valid_fomats[1]:
            for i, ID in enumerate(path_IDs_temp):
                f = h5py.File(ID, 'r')
                ret = np.array(f['patch']) #Key for matlab arrays is 'patch' because that's their name in the matlab code
                ret = ret.astype(np.float32)
                for j in range(self.n_channels): #This for-loop is needed because h5py opens .mat in 'channels first' format
                    Xnn[i, :, :, j] = ret[j]
                X[i, ] = self.normalize_input_data(Xnn[i, ])

        return X, None
