import keras.backend as K
import numpy as np
from keras.layers import Lambda, Dense, Input, Flatten
from keras.models import Model
from keras.losses import mse
from keras import callbacks
from importpatchesutil import ImportPatches
import matplotlib.pyplot as plt
import glob
import networks as nt

data_params = {'dim': (128, 128),
               'batch_size': 1,
               'n_classes': 2,
               'n_channels': 2,
               'fmt': 'mat',
               'norm_type': 'max1',
               'shuffle': True} #Dictionary containing the parameters for the data generator


'Model parameters'
input_shape = (*data_params['dim'], data_params['n_channels'])
original_dim = np.prod(input_shape)
intermediate_dim = 512
latent_dim = 2
mode = 'gauss'
args = [input_shape, original_dim, intermediate_dim, latent_dim]

'Compile model and callbacks'
encoder, decoder, vae = nt.autoencoder(args=args, mode=mode)
vae.compile(optimizer='adam')

terminate_on_nan = callbacks.TerminateOnNaN()
early_stop = callbacks.EarlyStopping(monitor='loss', patience=5, mode='min')
callbacks_list = [terminate_on_nan, early_stop]


if __name__ == '__main__':
    path = 'C:\\Users\\Vlad\\Desktop\\SatData\\SAR\\GRD\\Patches_mat\\*.mat'
    fls = glob.glob(path)
    ids = fls[:3]
    xtrain = ImportPatches(path_IDs=ids, **data_params)

    vae.fit_generator(generator=xtrain, use_multiprocessing=True, workers=6, epochs=3, callbacks=callbacks_list)
    # vae.save('gauss_vae_mlp_s1b20180823.h5')
    # encoder.save('enc_gauss_vae_mlp_s1b20180823.h5')
    # decoder.save('dec_gauss_vae_mlp_s1b20180823.h5')
    #plot_progress(vae_history)