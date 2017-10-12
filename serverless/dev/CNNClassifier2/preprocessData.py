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
from keras import backend as K
#import os
import numpy as np

#import matplotlib.pyplot as plt
#import scipy.io.wavfile as wav
# %matplotlib inline


# from python_speech_features import mfcc
# from python_speech_features import delta
# from python_speech_features import logfbank

from api import calculate_XY
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
numOfWavsForEachCategory = config.arc1Config['numOfWavsForEachCategory']

# Preprocessing data
wavDirBase = "Preproc"
x_all, y_all = calculate_XY(wavDirBase, categories, kernalSize, numOfWavsForEachCategory=numOfWavsForEachCategory)

print(x_all.shape)
print(y_all.shape)

np.savetxt("IEMOCAP_X", x_all)
np.savetxt("IEMOCAP_Y", y_all)

print("Datasets are created and saved successfully")
