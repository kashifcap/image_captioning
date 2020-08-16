# %%

# Importing generic python libraries
import string
import os
import math
import glob
import numpy as np
from numpy import array
import pandas as pd
import matplotlib.pyplot as plt
from time import time

# Importing libraries for image manipulation, deep-learning and pickling
from PIL import Image, ImageOps
from pickle import dump, load
import tensorflow as tf

# Importing functionalities from 'keras' library
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import LSTM, Embedding, TimeDistributed, Dense, RepeatVector, Activation, Flatten, Reshape, concatenate, Dropout, BatchNormalization
from keras.optimizers import Adam, RMSprop
from keras.layers.wrappers import Bidirectional
from keras.layers.merge import add
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras import Input, layers
from keras import optimizers
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.backend import set_session
from keras.utils import to_categorical

#%%
    
def generate_caption(filepath):
    
    # Importing custom modules

    from utils import image_processing
    from utils import caption_writer
    
    # Loading files to map predicted indices to words and vice-versa

    ixtoword=load(open('./resources/ixtoword.pkl','rb'))
    wordtoix=load(open('./resources/wordtoix.pkl','rb'))
    
    # Initializing and customizing the InceptionV3 Model

    model=InceptionV3(weights="imagenet")
    model_new=Model(model.input,model.layers[-2].output)
    
    # Loading pre-trained weights and compiling the model
    
    nlp_model=tf.keras.models.load_model('model_weights/final_model.h5')
    nlp_model.compile(loss='categorical_crossentropy',optimizer=tf.compat.v1.train.AdamOptimizer(learning_rate=0.0001))

    
    # Setting maximum length of caption
    max_length=72
    
    # Initializing empty dictionary for encoding custom images
    new_encoding_test={}
    
    # Selecting and processing single test image and mapping it into the encoding dictionary
    
    new_encoding_test[0]=image_processing.encode(filepath, model_new)
    
    # Reshaping encoded image and generating it's captions using 'nlp_model'
    
    image=new_encoding_test[0].reshape((1,2048))
    return(caption_writer.greedySearch(image, max_length, wordtoix, ixtoword, nlp_model))

    
# %%

#image_path = "1440465.jpg"
#caption = generate_caption(image_path)
#print(caption)