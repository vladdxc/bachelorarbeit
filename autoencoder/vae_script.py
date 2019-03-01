import keras.backend as K
import numpy as np
from keras.layers import Lambda, Dense, Input, Flatten
from keras.models import Model
from keras.losses import mse
from import_patches import ImportPatches
import glob


path = "D:\patches_S1B_IW_GRDH_20180823\*.tif"
fls = glob.glob(path)
len_path = len(fls)

params = {'dim': (128,128,2),
          'batch_size': 32,
          'n_classes': 1,
          'shuffle': True}
partition = {'train': fls}

def sampling(args):
    z_mean, z_log_var = args
    batch = K.shape(z_mean)[0]
    dim = K.int_shape(z_mean)[1]
    epsilon = K.random_normal(shape=(batch, dim))


    return z_mean + K.exp(0.5 * z_log_var) * epsilon

def elbo_loss(args):

    z_mean, z_log_var = args
    kl_loss = 1 + z_log_var - K.square(z_mean) - K.exp(z_log_var)
    kl_loss = K.sum(kl_loss, axis=-1)
    kl_loss *= -0.5

    return K.mean(kl_loss)

original_dim = 128*128*2
input_shape = (128,128,2)
intermediate_dim = 512
latent_dim = 2

inputs = Input(shape=input_shape, name='encoder_input')
flattened = Flatten()(inputs)
x = Dense(intermediate_dim, activation='relu')(flattened)
z_mean = Dense(latent_dim, name='z_mean')(x)
z_log_var = Dense(latent_dim, name='z_log_var')(x)

z = Lambda(sampling, output_shape=(latent_dim,), name='z')([z_mean, z_log_var])

encoder = Model(inputs, [z_mean, z_log_var, z], name='encoder')

latent_inputs = Input(shape=(latent_dim,), name='z_sampling')
x = Dense(intermediate_dim, activation='relu')(latent_inputs)
outputs = Dense(original_dim, activation='sigmoid')(x)
decoder = Model(latent_inputs, outputs, name='decoder')

outputs = decoder(encoder(inputs)[2])
vae = Model(inputs, outputs, name='vae_mlp')

encoder.summary()
decoder.summary()

reconstruction_loss = mse(flattened, outputs)
reconstruction_loss *= original_dim
elbo = elbo_loss([z_mean, z_log_var])

vae_loss = reconstruction_loss + elbo
vae.add_loss(vae_loss)

vae.compile(optimizer='adam')

if __name__ == '__main__':

    xtrain = ImportPatches(partition['train'], **params)
    vae.fit_generator(generator=xtrain, use_multiprocessing= True, workers= 3)
