"""""
This file contains the functions to instantiate different network architectures.
Also contains utility functions such as sampling and plotting network training results.

"""""
import keras.backend as K
from keras.layers import Lambda, Dense, Input, Flatten
from keras.models import Model
from keras.losses import mse
import numpy as np
import matplotlib.pyplot as plt

def autoencoder(args, mode):

    def get_batch_dim(param):
        btch = K.shape(param)[0]
        dm = K.int_shape(param)[1]
        return btch, dm

    'Initialize supported modes and kl-divergence and get arguments'
    supported_modes = ['gauss', 'rayleigh', 'exponential', 'gamma']
    input_shape, original_dim, intermediate_dim, latent_dim = args

    'Input and flatten layers'
    inputs = Input(shape=input_shape, name='encoder_input')
    flattened = Flatten()(inputs)
    x = Dense(intermediate_dim, activation='relu')(flattened)

    if mode not in supported_modes or mode == supported_modes[0]:
        'Gauss encoder'
        def sampling(sampl_args):
            'Sample from an isotropic gaussian using the reparametrization trick'
            z_mean, z_log_var = sampl_args
            batch, dim = get_batch_dim(z_mean)
            epsilon = K.random_normal(shape=(batch, dim))
            return z_mean + K.exp(0.5 * z_log_var) * epsilon

        z_mean = Dense(latent_dim, name='z_mean')(x)
        z_log_var = Dense(latent_dim, name='z_log_var')(x)

        z = Lambda(sampling, output_shape=(latent_dim,), name='z')([z_mean, z_log_var])
        encoder = Model(inputs, [z_mean, z_log_var, z], name='gauss_encoder')
        kl = -0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=-1)

    elif mode == supported_modes[1]:
        def sampling(sampl_args):
            z_sigma_sq = sampl_args
            batch, dim = get_batch_dim(z_sigma_sq)
            epsilon = K.random_uniform(shape=(batch, dim))
            return K.sqrt(-2*z_sigma_sq*K.log(1 - epsilon))
        z_sigma_sq = Dense(latent_dim, name='z_sigma_squared')(x)
        z = Lambda(sampling, output_shape=(latent_dim,), name='z')([z_sigma_sq])
        encoder = Model(inputs, [z_sigma_sq, z], name='rayleigh_encoder')
        'We suppose p_theta(z) has sigma_sq parameter 1'
        kl = -1*K.sum(-1*K.log(z_sigma_sq) + 2*z_sigma_sq - 1, axis= -1)

    elif mode == supported_modes[2]:
        def sampling(sampl_args):
            z_lambda = sampl_args
            batch, dim = get_batch_dim(z_lambda)
            epsilon = K.random_uniform(shape=(batch, dim))
            return (1/z_lambda) + K.log(1 - epsilon)
        z_lambda = Dense(latent_dim, name='z_lambda')(x)
        z = Lambda(sampling, output_shape=(latent_dim,), name='z')([z_lambda])
        encoder = Model(inputs, [z_lambda, z], name='exponential_encoder')
        'We suppose p_theta(z) has lambda parameter 1'
        kl = -1*K.sum(-2*z_lambda - 2, axis=-1)

    elif mode == supported_modes[3]:
        return 'Gamma distribution is not yet implemented!'


    latent_inputs = Input(shape=(latent_dim,), name='z_sampling')
    x = Dense(intermediate_dim, activation='relu')(latent_inputs)
    outputs = Dense(original_dim, activation='sigmoid', name='decoder_output')(x)
    decoder = Model(latent_inputs, outputs, name='decoder')

    outputs = decoder(encoder(inputs)[2])
    vae = Model(inputs, outputs, name='vae_mlp')
    rec = mse(K.flatten(inputs), K.flatten(outputs))

    'Construct loss function using the mse and the kl-divergence'

    vae_loss = K.mean(kl + rec)
    vae.add_loss(vae_loss)

    return encoder, decoder, vae


def plot_progress(history):
    'Plot training progress'
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()


def visualization_transform(arr, args):
    'Generated data is transformed in such a way that it can be interpreted visually.'
    alpha, beta = args
    imglog = alpha*np.log(beta*arr)
    mu = np.mean(imglog)
    sigma = np.std(imglog)
    imglogstd = np.divide(imglog - mu, sigma)
    transformed = 255 * imglogstd
    return transformed
