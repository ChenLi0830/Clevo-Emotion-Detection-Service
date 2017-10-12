from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D, Input, AveragePooling2D
from keras import backend as K
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav


# from python_speech_features import mfcc
# from python_speech_features import delta
# from python_speech_features import logfbank

from api import readFileAndAggregateUtterance, getFeature, calculate_XY, conv2D_AvePool
from keras.utils.np_utils import to_categorical
import python_speech_features
import datetime

import config
# model params
batch_size = config.arc1Config['batch_size']
categories = config.arc1Config['categories']
epochs = config.arc1Config['epochs']
kernalSize = config.arc1Config['kernalSize']
num_classes = config.arc1Config['num_classes']

def build_index_label(pred, label_list):
    a = max([(v,i) for i,v in enumerate(pred)])
    idx = a[1]
    return label_list[idx]

lastModel = load_model('emotion_model.h5')
lastModel.load_weights('emotion_model_weights.h5')

# newWavPath = "Preproc/Sadness/Ses01F_impro02_F010.wav"
# newWavPath = "Preproc/Happiness/Ses01F_impro03_F008.wav"
# newWavPath = "Preproc/Neutral/Ses01F_impro03_M021.wav"
# newWavPath = "Preproc/Anger/Ses02M_script03_2_M039.wav"
# newWavPath = "Preproc/Sadness/Ses04M_script01_3_M025.wav"
# newWavPath = "Preproc/Neutral/Ses05M_impro05_M009.wav"
# newWavPath = "Preproc/Neutral/Ses05M_impro05_M009.wav"

# Ses01F_impro02_F004.wav
# Ses01F_impro02_F005.wav
# Ses01F_impro02_F007.wav
# Ses01F_impro02_F008.wav
# Ses01F_impro02_F010.wav
# Ses01F_impro02_F012.wav
# Ses01F_impro02_F013.wav
# Ses01F_impro02_F014.wav
result = conv2D_AvePool(newWavPath, kernalSize)
print("result.shape", result.shape)

pred_result = lastModel.predict(np.reshape(result, (1,kernalSize)), batch_size)[0]
print(pred_result)
print("Prediction result: {}".format(build_index_label(pred_result, categories)))
