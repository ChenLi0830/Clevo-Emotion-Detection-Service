#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:26:02 2017

@author: wangwei
"""

import os

from keras.models import load_model


import librosa
import scipy.io.wavfile as wav
import scipy
import numpy as np
from api import segment_wav_may
#from main import getMelspectrogram, build_index_label, predict_3s, predict_module
#from main import predict_module
import main as app

#def predict_module(url,model,jsonArr):
#            
#    # define downloaded filename
#    filename = url
#
#    segment_wav_may(jsonArr, filename,'save')
#    for seg_wavfile in os.listdir('save'):
#        predict_3s(os.path.join('save',seg_wavfile), model)


def kernel():

    ##############################
    model = load_model('emotion_model.h5')
    model.load_weights('emotion_model_weights.h5')
    # url = "https://s3-us-west-2.amazonaws.com/clevo.data/temp/Ses01M_impro04_F006.wav"
    jsonArr = [{"bg":"180","ed":"3620","onebest":"你好，周六为您服务，请问什么可以帮你？","speaker":"1"},{"bg":"4080","ed":"11950","onebest":"唉你好，那个我想问一下我这个课堂有一个15块钱的支付那个脉动是吧？","speaker":"2"},{"bg":"11970","ed":"16860","onebest":"我不知道，我跟你帮我查一下是来电，这个11的手机号码嘛。","speaker":"1"},{"bg":"17820","ed":"22120","onebest":"嗯来电这个手机号码吗？","speaker":"2"},{"bg":"22230","ed":"42270","onebest":"对对对有钱烧的我这边帮您看一下您好先生抱歉让您久等了我这边看到6月19份6月19号一共有两笔交易一笔成功的1:4兆的成功的这里是一个常州A图A图游戏15元礼包这个是按次点播的游戏你点过一次收一次费用不点拨不收取任何费用的","speaker":"1"},{"bg":"42810","ed":"72600","onebest":"这个是属于咱们我的我我无意当中点的，我觉得本身属于暗示点拨的游戏，如果你以后不想再产生相应费用的话，我这边可以给你手机号码对一下号码保护处理。如果通过我是平台就是话费再也不能购买任何游戏上面应该需要做保护吗先生那你除了保护之外能把这四块钱能够对未来不这个抱歉真的15块钱在当时都已经支付成功了，我能做的话就是您说一下照顾bb","speaker":"1"},{"bg":"72610","ed":"76320","onebest":"以后再产生类似扣费你还需要做保护吗？","speaker":"1"},{"bg":"76500","ed":"91820","onebest":"那我找10086还能能够对我来说这个抱歉，这个是你那个是按次点播的游行点播一次收一次费用，不点拨不出去了，费用我这个也不知道，我这边只能给你说一下保护，避免以后再产生类似的口碑","speaker":"1"},{"bg":"92160","ed":"98620","onebest":"好的你拿着礼物帮我宝贝原来已经把我好了，什么还有什么，其他能帮你把24小时等一下","speaker":"1"},{"bg":"98990","ed":"101390","onebest":"没有了就之前。","speaker":"1"}]
    # use real URL
    url = "https://s3-us-west-2.amazonaws.com/clevo.data/wav/20170623095248_956_15140969348_601.wav"
    #    url = "20170623095248_956_15140969348_601.wav"
    app.predict_module(url, model, jsonArr)
    
kernel()