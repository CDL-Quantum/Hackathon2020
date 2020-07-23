import tensorflow as tf
import numpy as np
import random
import time
import os

from tensorflow.keras import layers
enigma = None

class GAN:
    
    def __init__(self, model_path = 'Model/'):
        self.model_path = model_path
        self.enigma = None
        
    def load_model(self):
        self.enigma = tf.keras.models.load_model(self.model_path, compile=False)

    def predict(self, number_preds):

        #output list
        output = []
        for i in range(number_preds):
            noise = tf.random.normal([1, 100])
            cat = self.enigma(noise, training=False)
            kitty = tf.reshape(cat, [24,24])
            fluff = tf.math.greater(kitty, 0.5)
            puff = tf.cast(fluff, tf.int32)
            output.append(puff)

        return output