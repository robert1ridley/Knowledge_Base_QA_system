from keras.layers import Dense, Input, Embedding, Dropout
from keras.models import Model
from keras.layers.convolutional import Convolution1D
from keras.engine.topology import Layer
import time
import keras.backend as K
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)


class Conv1DWithMasking(Convolution1D):
    def __init__(self, **kwargs):
        self.supports_masking = True
        super(Conv1DWithMasking, self).__init__(**kwargs)

    def compute_mask(self, x, mask):
        return mask


class MeanPool(Layer):
  def __init__(self, **kwargs):
      self.supports_masking = True
      super(MeanPool, self).__init__(**kwargs)

  def compute_mask(self, input, input_mask=None):
      return None

  def call(self, x, mask=None):
      if mask is not None:
          mask = K.cast(mask, K.floatx())
          mask = K.repeat(mask, x.shape[-1])
          mask = tf.transpose(mask, [0,2,1])
          x = x * mask
      return K.sum(x, axis=1) / K.sum(mask, axis=1)

  def compute_output_shape(self, input_shape):
      return (input_shape[0], input_shape[2])


def build_convolutional_network(max_sent, emb_dim, y_size):
    text_input = Input(shape=(max_sent,), dtype='int32', name='text_input')
    emb_layer = Embedding(output_dim=emb_dim, input_dim=emb_dim, input_length=max_sent,
                  mask_zero=True, name='pos_emb')(text_input)
    conv_layer = Conv1DWithMasking(nb_filter=50, filter_length=5, border_mode='same',
                                   subsample_length=1, name='conv_layer')(emb_layer)
    pooling = MeanPool(name='pooling')(conv_layer)
    drop_layer = Dropout(0.1, name='drop_layer')(pooling)

    y = Dense(y_size, activation='sigmoid', name='output')(drop_layer)

    model = Model(inputs=text_input, outputs=y)

    start_time = time.time()
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    total_time = time.time() - start_time
    print("Model compiled in {} s".format(total_time))

    model.summary()

    return model

