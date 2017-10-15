#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 12:18:25 2017

@author: admin
"""

from __future__ import print_function
# import keras
from keras import optimizers
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Activation, Conv2D, MaxPooling2D
from keras.callbacks import EarlyStopping, ModelCheckpoint
# from keras.layers import Conv2D, MaxPooling2D, Input, AveragePooling2D
# from keras import backend as K
# import os
import numpy as np
from sklearn.utils import class_weight
from sklearn.model_selection import train_test_split
import os
# import matplotlib.pyplot as plt
# import scipy.io.wavfile as wav
# %matplotlib inline


# from python_speech_features import mfcc
# from python_speech_features import delta
# from python_speech_features import logfbank

# from preprocessing import readFileAndAggregateUtterance, getFeature, calculate_XY, conv2D_AvePool
from keras.utils.np_utils import to_categorical
# import python_speech_features
import config

# model params
batch_size = config.arc1Config['batch_size']
categories = config.arc1Config['categories']
epochs = config.arc1Config['epochs']
kernalSize = config.arc1Config['kernalSize']
num_classes = config.arc1Config['num_classes']
architecture = config.arc1Config['architecture']
archNames = config.arc1Config['archNames']
numOfWavsForEachCategory = config.arc1Config['numOfWavsForEachCategory']
# print("batch_size, categories, epochs, kernalSize, num_classes", batch_size, categories, epochs, kernalSize, num_classes)


# from api import calculate_XY
# # Preprocessing data
# wavDirBase = "Preproc"
# x_all, y_all = calculate_XY(wavDirBase, categories, kernalSize, numOfWavsForEachCategory=numOfWavsForEachCategory,
#                             architecture=architecture)

# Load data
x_all = np.load("IEMOCAP_X.npy")
y_all = np.load("IEMOCAP_Y.npy")


X_train, X_test, Y_train, Y_test = train_test_split(x_all, y_all, test_size=0.2, random_state=0)
Y_train_cat = to_categorical(Y_train)
Y_test_cat = to_categorical(Y_test)

print(X_train.shape)
print(Y_train_cat.shape)

# Build modal
print("Using model {}: {}".format(architecture, archNames[architecture]))
if architecture == 0:
    lastModel = Sequential()
    lastModel.add(Dense(units=num_classes, input_dim=x_all.shape[1], activation='softmax'))
    lastModel.compile(loss='categorical_crossentropy',
                      # optimizer=adam,
                      # optimizer='rmsprop',
                      optimizer='adam',
                      metrics=['accuracy'])

elif architecture == 1:
    lastModel = Sequential()
    print("x_all.shape[1]", x_all.shape[1])
    lastModel.add(Dense(units=8, input_dim=x_all.shape[1], activation='relu'))
    lastModel.add(Dense(units=4, activation='relu'))
    # lastModel.add(Dense(units=4, input_dim=4))
    # lastModel.add(Dense(units=8, input_dim=8))
    lastModel.add(Dense(units=num_classes, activation='softmax'))
    # lastModel.add(Activation('softmax'))
    # print()
    lastModel.compile(loss='categorical_crossentropy',
                      # optimizer=adam,
                      # optimizer='rmsprop',
                      optimizer='adam',
                      metrics=['accuracy'])

elif architecture == 2:
    lastModel = Sequential()
    lastModel.add(Dense(units=num_classes, input_dim=kernalSize))
    # lastModel.add(Dense(units=512, input_dim=kernalSize))
    # lastModel.add(Dense(units=num_classes, input_dim=512))
    lastModel.add(Activation('softmax'))
    # lastModel.add(Dense(10, activation='softmax'))

    # sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    # adam = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

    lastModel.compile(loss='categorical_crossentropy',
                      # optimizer=adam,
                      optimizer='rmsprop',
                      # optimizer='adam',
                      metrics=['accuracy'])

elif architecture == 3:
    lastModel = Sequential()
    print("x_all.shape[1]", x_all.shape[1])
    lastModel.add(Dense(units=32, input_dim=x_all.shape[1], activation='relu'))
    lastModel.add(Dense(units=16, activation='relu'))
    lastModel.add(Dense(units=8, activation='relu'))
    # lastModel.add(Dense(units=4, input_dim=4))
    # lastModel.add(Dense(units=8, input_dim=8))
    lastModel.add(Dense(units=num_classes, activation='softmax'))
    # lastModel.add(Activation('softmax'))
    # print()
    lastModel.compile(loss='categorical_crossentropy',
                      # optimizer=adam,
                      # optimizer='rmsprop',
                      optimizer='adam',
                      metrics=['accuracy'])

elif architecture == 4:
    lastModel = Sequential()
    print("x_all.shape[1]", x_all.shape[1])
    # x_all.reshape(-1, 128, 1500, 1)

    # lastModel.add(Conv2D(64, (3, 3), padding="same"))
    # lastModel.add(Activation('relu'))
    # lastModel.add(MaxPooling2D(pool_size=(2, 2), padding="same"))

    lastModel.add(Conv2D(32, (3, 3), input_shape=(x_all[0].shape[0], x_all[0].shape[1], 1), padding="same"))
    lastModel.add(MaxPooling2D(pool_size=(2, 2), padding="same"))
    lastModel.add(Activation('relu'))

    # lastModel.add(Conv2D(32, (3, 3), padding="same"))
    # lastModel.add(MaxPooling2D(pool_size=(2, 2), padding="same"))
    # lastModel.add(Activation('relu'))
    #
    # lastModel.add(Conv2D(64, (3, 3), padding="same"))
    # lastModel.add(MaxPooling2D(pool_size=(2, 2), padding="same"))
    # lastModel.add(Activation('relu'))

    lastModel.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
    lastModel.add(Dense(128))
    lastModel.add(Activation('relu'))
    lastModel.add(Dropout(0.5))
    lastModel.add(Dense(units=num_classes, activation='softmax'))

    lastModel.compile(loss='categorical_crossentropy',
                      # optimizer=adam,
                      # optimizer='rmsprop',
                      optimizer='adam',
                      metrics=['accuracy'])

# Balance dataset using weight
class_weight = class_weight.compute_class_weight('balanced', np.unique(Y_train), Y_train)
class_weight_dict = dict(enumerate(class_weight))
# for i, v in enumerate(class_weight):
#     class_weight_dict[i] = v
print("class_weight_dict", class_weight_dict)
# Train modal

X_train = X_train.reshape(-1, X_train.shape[1], X_train.shape[2], 1)
X_test = X_test.reshape(-1, X_test.shape[1], X_test.shape[2], 1)

# callbacks
esCallback = EarlyStopping(monitor='val_loss',
                              min_delta=0,
                              patience=10,
                              verbose=1, mode='auto')

saveModelFilePath = "savedModel"
if os.path.exists(saveModelFilePath) != True:
    print("Creating dir: " + saveModelFilePath)
    os.makedirs(saveModelFilePath)

savedModelPath = saveModelFilePath+"/weights.best.hdf5"

checkpoint = ModelCheckpoint(savedModelPath, monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='max', period=1)

# fit model
lastModel.fit(X_train, Y_train_cat, batch_size=batch_size, epochs=epochs, verbose=1, validation_split=0.2,
              class_weight=class_weight_dict, callbacks=[checkpoint, esCallback])

print("Loading best model weight...")
lastModel.load_weights(savedModelPath)
# Test modal
score = lastModel.evaluate(X_test, Y_test_cat, verbose=0)
print('Test loss:', score[0])
print('Test Unweighted accuracy:', score[1])


# y_pred = lastModel.predict(X_test)
# acc = sum([np.argmax(Y_test_cat[i])==np.argmax(y_pred[i]) for i in range(len(X_test))])/len(X_test)
# print('Real test accuracy:', acc)
y_pred = lastModel.predict(X_test)
WeightedAccuracyArr = np.zeros(num_classes)
count = np.zeros(num_classes)
for i in range(len(X_test)):
    categoryIdx = np.argmax(Y_test_cat[i])
    WeightedAccuracyArr[categoryIdx] += np.argmax(Y_test_cat[i]) == np.argmax(y_pred[i])
    count[categoryIdx] += 1
WeightedAccuracyArr = WeightedAccuracyArr / count

print("Weighted category counts", count)
print("WeightedAccuracyArr", WeightedAccuracyArr)
print("Weighted Accuracy: ", sum(WeightedAccuracyArr) / num_classes)

# Save modal
lastModel.save('emotion_model.h5')  # creates a HDF5 file 'my_model.h5'
lastModel.save_weights('emotion_model_weights.h5')
