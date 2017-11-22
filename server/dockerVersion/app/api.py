from flask import Flask
from flask import request

app = Flask(__name__)

# from api import getMelspectrogram
import urllib.request
import librosa
import scipy.io.wavfile as wav
import scipy
import os
from scipy.io import wavfile
import numpy as np
import sys
import re
import json as jsonLibrary
from array_split import shape_split
from emotion import Emotion

from keras import backend as K
from keras.models import load_model

model = None

print("os.environ['fast_disk_path']", os.environ['fast_disk_path'], file=sys.stdout)


def segment_wav_by_sentence(speech_transcription, path):
    if os.path.exists(path) != True:
        raise ValueError("audio path doesn't exist")
    # todo: check if it is .wav file
    [sampleRate, audio] = wavfile.read(path)
    # print("sampleRate, len(audio)", sampleRate, len(audio))
    for i, json in enumerate(speech_transcription):
        begin = int(int(json['bg']) * sampleRate / 1000)
        end = int(int(json['ed']) * sampleRate / 1000)
        audioSeg = audio[begin:end]
        filePrefix = os.path.basename(path).split('.')[0]
        savePath = os.environ['fast_disk_path']
        if not os.path.isdir(savePath):
            os.makedirs(savePath)
        newFilePath = "{}/{}__{}.wav".format(savePath, filePrefix, str(i))
        wavfile.write(newFilePath, sampleRate, np.array(audioSeg, dtype="int16"))
        # return []


def segment_wav_by_seconds(speech_transcription, file_path, savePath=os.environ['fast_disk_path'], low_th=3, high_th=6):
    speech_transcription_list = jsonLibrary.loads(re.sub(r'\'', '"', speech_transcription))

    # print('len(speech_transcription_list)', len(speech_transcription_list))
    # print('speech_transcription_list', speech_transcription_list, file=sys.stdout)


    if not os.path.exists(file_path):
        raise ValueError("audio file_path doesn't exist")
    # todo: check if it is .wav file

    [sampleRate, audio] = wavfile.read(file_path)
    # print("sampleRate, len(audio)", sampleRate, len(audio), file=sys.stdout)

    filePrefix = os.path.basename(file_path).split('/')[-1].split('.')[0]


    # print('segment_wav_by_seconds savePath', savePath, file=sys.stdout)
    if not os.path.isdir(savePath):
        print("savePath {} doesn't exist, creating savePath".format(savePath), file=sys.stdout)
        os.makedirs(savePath)
        if not os.path.isdir(savePath):
            print("Error, savePath can't be created!", file=sys.stdout)
            return
            # print("Error, savePath can't be created!")

    # save the files segmented in 3-6 seconds
    new_files_path = []
    for i, json in enumerate(speech_transcription_list):
        begin = int(int(json['bg']) * sampleRate / 1000)
        end = int(int(json['ed']) * sampleRate / 1000)
        time_span = (int(json['ed']) - int(json['bg'])) / 1000
        audioSeg = audio[begin:end]

        if time_span < low_th:
            """remove sentence audio if it is too short e.g., < 3 s"""
            continue
        elif time_span <= high_th:
            """save audio file to the savePath if it is between 3s and 6s
               File format : savePath/originalFileName_speaker_begin_end.wav
            """
            newFilePath = "{}/{}__sp{}__beg{}_end{}.wav".format(savePath, filePrefix, json['speaker'], str(json['bg']),
                                                                str(json['ed']))
            wavfile.write(newFilePath, sampleRate, np.array(audioSeg, dtype="int16"))
            new_files_path.append(newFilePath)
        else:
            """For sentence audio that is longer than 6s, we divide it equally into '3s' sub-segments
               File format : savePath/originalFileName_speaker_begin_end.wav
               E.g., audio = wavfile.read(originalFileName)
                     sent_audio = audio[begin:end]
            """
            segs = int(int(time_span) / low_th)

            slice_array = shape_split(audioSeg.shape, segs)
            for i in range(segs):
                b = slice_array[i][0]
                # print(b.start, b.stop)
                audioSeg_seg = audio[begin + b.start: begin + b.stop]
                newFilePath = "{}/{}__sp{}__beg{}_end{}.wav".format(savePath, filePrefix, json['speaker'],
                                                                    str(int((begin + b.start) * 1000 / sampleRate)), str(int((begin + b.stop) * 1000 / sampleRate)))
                wavfile.write(newFilePath, sampleRate, np.array(audioSeg_seg, dtype="int16"))
                new_files_path.append(newFilePath)

    return new_files_path


def getMelspectrogram(wavPath):
    if not os.path.exists(wavPath):
        raise ValueError("Error, wavPath doesn't exist!")
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
    a = max([(v, i) for i, v in enumerate(pred[0])])
    idx = a[1]

    return label_list[idx]


def predict_3s(wavPath):
    global model

    if not model:
        # Load model
        print("Loading model", file=sys.stdout)
        model = load_model('emotion_model.h5')
        model.load_weights('emotion_model_weights.h5')

    # get data to be predicted X_pred
    result = getMelspectrogram(wavPath)

    if len(result) == 0:
        print("wavPath too long/short")
        return "wavPath too long/short"
    else:
        inputData = result.reshape(1, result.shape[0], result.shape[1], 1)

        result = model.predict(inputData)

        label_list = ["Angry", "Not Angry"]

        response = build_index_label(result, label_list)
        # print(response)
        return response, result[0].tolist()


def predict_module(url, speech_transcription):
    print('url', url, file=sys.stdout)
    # print(speech_transcription, file=sys.stdout)
    # define downloaded filename
    filename = "/tmp.wav"

    # download file from url and save to 'filename'
    try:
        urllib.request.urlretrieve(url, filename)
    except Exception as e:
        return "Can't access the audio url you provide"


    file_paths = segment_wav_by_seconds(speech_transcription, filename, os.environ['fast_disk_path'])
    # print('file_paths', file_paths, file=sys.stdout)
    arr = []

    for seg_wav_file_path in file_paths:

        # tag, prob = predict_3s(os.path.join(segmentPath, seg_wavfile))
        tag, prob = predict_3s(seg_wav_file_path)

        file_name_meta = seg_wav_file_path.split('/')[-1].split('_')

        result = Emotion(
            begin=file_name_meta[-2].replace('beg', ''),
            end=file_name_meta[-1].split('.')[0].replace('end', ''),
            prob=prob,
            tag=tag,
        )

        arr.append(result)

    # remove tmp files
    for file_path in file_paths:
        os.remove(file_path)

    return arr
