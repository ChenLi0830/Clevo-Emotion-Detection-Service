#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 12:18:25 2017

@author: admin
"""

from __future__ import print_function
#import keras
#from keras.datasets import mnist
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Activation
#from keras.layers import Conv2D, MaxPooling2D, Input, AveragePooling2D
#from keras import backend as K
#import os
import numpy as np

#import matplotlib.pyplot as plt
#import scipy.io.wavfile as wav
# %matplotlib inline


# from python_speech_features import mfcc
# from python_speech_features import delta
# from python_speech_features import logfbank

#from preprocessing import readFileAndAggregateUtterance, getFeature, calculate_XY, conv2D_AvePool
from keras.utils.np_utils import to_categorical
#import python_speech_features
import config
# model params
batch_size = config.arc1Config['batch_size']
categories = config.arc1Config['categories']
epochs = config.arc1Config['epochs']
kernalSize = config.arc1Config['kernalSize']
num_classes = config.arc1Config['num_classes']
# print("batch_size, categories, epochs, kernalSize, num_classes", batch_size, categories, epochs, kernalSize, num_classes)

# Preprocessing data
wavDirBase = "Preproc"

# Load data
x_all = np.loadtxt("IEMOCAP_X")
y_all = np.loadtxt("IEMOCAP_Y")

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(x_all, y_all, test_size=0.2, random_state=0)
Y_train_cat = to_categorical(Y_train)
Y_test_cat = to_categorical(Y_test)

print(X_train.shape)
print(Y_train_cat.shape)

# Build modal
lastModel = Sequential()
lastModel.add(Dense(units=num_classes, input_dim=kernalSize))
# lastModel.add(Dense(units=512, input_dim=kernalSize))
# lastModel.add(Dense(units=num_classes, input_dim=512))
lastModel.add(Activation('softmax'))
# lastModel.add(Dense(10, activation='softmax'))
# lastModel.compile(loss='categorical_crossentropy',
#               optimizer='rmsprop',
#             #   optimizer='adam',
#               metrics=['accuracy'])
lastModel.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
            #   optimizer='adam',
              metrics=['accuracy'])


# Train modal
lastModel.fit(X_train, Y_train_cat, batch_size=batch_size, epochs=epochs, verbose=1, validation_split=0.2)
# Test modal
score = lastModel.evaluate(X_test, Y_test_cat, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# Save modal
lastModel.save('emotion_model.h5')  # creates a HDF5 file 'my_model.h5'
lastModel.save_weights('emotion_model_weights.h5')
