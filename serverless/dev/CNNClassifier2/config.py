#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 13:45:20 2017

@author: admin
"""

# model params
arc1Config = {
    'batch_size': 128,
    'categories': ["Anger", "Happiness", "Neutral", "Sadness"],
    'epochs': 5000,
    'kernalSize': 180,
    'numOfWavsForEachCategory': 200,
    'archNames': {0: "AvePool, Softmax", 1: "AvePool, 8+4, Softmax; ", 2: "Conv2D, AvePool, Softmax", 3: "AvePool, 32+16+8, Softmax", 4: "MelSpectrogram+Padding, Conv2D+Conv2D.., Softmax"},
    'architecture': 4,
}

arc1Config['num_classes'] = len(arc1Config['categories'])
