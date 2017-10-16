#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 12:18:25 2017

@author: admin
"""

from __future__ import print_function
import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
import config
import api
import sklearn
import matplotlib.pyplot as plt

# model params
batch_size = config.arc1Config['batch_size']
categories = config.arc1Config['categories']
epochs = config.arc1Config['epochs']
kernalSize = config.arc1Config['kernalSize']
num_classes = config.arc1Config['num_classes']
architecture = config.arc1Config['architecture']
archNames = config.arc1Config['archNames']
numOfWavsForEachCategory = config.arc1Config['numOfWavsForEachCategory']

# Load data
x_all = np.load("IEMOCAP_X.npy")
y_all = np.load("IEMOCAP_Y.npy")

X_trainValid, X_test, Y_trainValid, Y_test = train_test_split(x_all, y_all, test_size=0.2, random_state=0)
X_train, X_valid, Y_train, Y_valid = train_test_split(X_trainValid, Y_trainValid, test_size=0.2, random_state=0)

# # Generate training data
# X_train, Y_train = api.generateData(X_train, Y_train, batch_size=16, width_shift_range=0.2, zoom_range=0.1)

# reshape data
X_train = X_train.reshape(-1, X_train.shape[1], X_train.shape[2], 1)
X_valid = X_valid.reshape(-1, X_valid.shape[1], X_valid.shape[2], 1)
X_test = X_test.reshape(-1, X_test.shape[1], X_test.shape[2], 1)

Y_train_cat = to_categorical(Y_train)
Y_valid_cat = to_categorical(Y_valid)
Y_test_cat = to_categorical(Y_test)

print("X_train.shape", X_train.shape)
print("Y_train.shape", Y_train.shape)
print("Y_train_cat.shape", Y_train_cat.shape)

print("Using model {}: {}".format(architecture, archNames[architecture]))

# Balance dataset using weight
class_weight = sklearn.utils.class_weight.compute_class_weight('balanced', np.unique(Y_train), Y_train)
class_weight_dict = dict(enumerate(class_weight))
# for i, v in enumerate(class_weight):
#     class_weight_dict[i] = v
print("class_weight_dict", class_weight_dict)

# # Calculate accuracies
# api.trainNetwork(X_train, Y_train_cat, X_valid, Y_valid_cat, X_test, Y_test_cat, architecture, num_classes, kernalSize,
#                  batch_size, epochs, class_weight_dict)

# Calculate learning curve
train_sizes = (len(X_train) * np.linspace(0.1, 0.999, 4)).astype(int)
print("train_sizes", train_sizes)

unweighted_acc_scores = []
weighted_acc_scores = []

for train_size in train_sizes:
    X_train_frac, _, Y_train_frac, _ = \
        train_test_split(X_train, Y_train, train_size=train_size)

    unweightedAcc, weightedAcc = api.trainNetwork(X_train_frac, Y_train_frac, X_valid, Y_valid_cat, X_test, Y_test_cat,
                                                  architecture, num_classes, kernalSize, batch_size, epochs,
                                                  class_weight_dict)

    unweighted_acc_scores.append(unweightedAcc)
    weighted_acc_scores.append(weightedAcc)

    print("Done size: ", train_size)

plt.plot(train_sizes, unweighted_acc_scores, 'o-', label="unweighted_acc_scores")
plt.plot(train_sizes, weighted_acc_scores, 'o-', label="weighted_acc_scores")
plt.legend(loc="best")
