#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf-8

from flask import Flask
from flask import request
app = Flask(__name__)

import os
import imp
from keras import backend as K
from keras.models import load_model

# from api import getMelspectrogram
import urllib.request
import librosa
import scipy.io.wavfile as wav
import scipy
import numpy as np
# def set_keras_backend(backend):
#     if K.backend() != backend:
#         os.environ['KERAS_BACKEND'] = backend
#         imp.reload(K)
#         assert K.backend() == backend

from keras.preprocessing import sequence
from keras.models import model_from_json

def getMelspectrogram(wavPath):
    if os.path.exists(wavPath) == False:
        print("Error, wavPath doesn't exist!")
        return
    (rate, sig) = wav.read(wavPath)
    # # Features: mel-spectrogram
    # features = librosa.feature.melspectrogram(y=sig, sr=rate, fmin=50, fmax=3000)

    if (sig.shape[0] / rate > 10) or (sig.shape[0] / rate < 2):
        return []

    features = librosa.feature.melspectrogram(y=sig, sr=rate, fmin=50, fmax=3000)
    # power to DB
    features = librosa.power_to_db(features, ref=np.max)

    features = scipy.misc.imresize(features, (features.shape[0], 300))

    # Normalization - faster learning rate, higher accuracy
    features = features / np.max(features)

    return features

def build_index_label(pred, label_list):
    a = max([(v,i) for i,v in enumerate(pred[0])])
    idx = a[1]

    return label_list[idx]

@app.route("/",methods=['GET','POST'])
def hello():
    print("request", request)
    model = load_model('emotion_model.h5')
    model.load_weights('emotion_model_weights.h5')

    try:
        url = request.form['audioURL']
        print("audioURL", url)
    except Exception as e:
        # print("error", e)
        return "An url of audio file is required in the request"

    # url = "https://s3-us-west-2.amazonaws.com/clevo.data/temp/Ses01M_impro04_F006.wav"
    filename = "/tmp.wav"

    try:
        urllib.request.urlretrieve(url, filename)
    except Exception as e:
        return "Can't access the audio url you provide"

    wavPath = filename

    result = getMelspectrogram(wavPath)

    if len(result) == 0:
        print("wavPath too long")
        return "wavPath too long/short"
    else:
        inputData = result.reshape(1, result.shape[0], result.shape[1], 1)

        result = model.predict(inputData)

        print(result)
        # print("actual result: {}".format(y_all[index]))
        label_list = ["Angry", "Not Angry"]

        response = build_index_label(result, label_list)
        print(response)
        return response

if __name__ == "__main__":
	#decide what port to run the app in
	# port = int(os.environ.get('PORT', 80))
    # app.run(host='127.0.0.1', port=port)
	#run the app locally on the givn port

    app.run(host='0.0.0.0', debug=True, port=80)
    #optional if we want to run in debugging mode
	#app.run(debug=True)


K.clear_session()

