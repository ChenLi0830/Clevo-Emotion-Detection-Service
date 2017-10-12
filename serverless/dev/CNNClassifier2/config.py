#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 13:45:20 2017

@author: admin
"""

# model params
arc1Config = {'batch_size': 128,
              'categories': ["Anger", "Happiness", "Neutral", "Sadness"],
              'epochs':500,
              'kernalSize':18}

arc1Config['num_classes'] = len(arc1Config['categories'])
