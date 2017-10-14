import shutil
import re
import os
import numpy as np
import python_speech_features
import scipy.io.wavfile as wav
from keras import initializers, backend as K
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D, Input, AveragePooling2D
import datetime
from pyAudioAnalysis import audioFeatureExtraction
import librosa
import librosa.display
import scipy

def placeUtteranceToFolder(wavPath, category, savePath):
    catePath = savePath + "/" + category
    if (os.path.exists(wavPath) != True):
        raise ValueError("wavPath doesn't exist")
    if (os.path.exists(savePath) != True):
        print("Creating dir: " + savePath)
        os.makedirs(savePath)
    if (os.path.exists(catePath) != True):
        print("Creating dir: " + catePath)
        os.makedirs(catePath)

    filename = os.path.basename(wavPath)

    shutil.copy2(wavPath, catePath)  # complete target filename given

    print("{} is put into path: {}".format(filename, catePath))


def readFileAndAggregateUtterance(filePath, wavDir, relativeSavePath, percentage=0.6):
    categories = ['Neutral', 'Anger', 'Frustration', 'Sadness', 'Happiness']
    wavDirPath = "/Users/Chen/百度云同步盘/Startup/Clevo/数据/IEMOCAP_full_release/EmotionRecognization/wav/"

    with open(filePath) as f:
        wav_basename = ""
        count = 0
        # cateStats = {'Neutral': 0, 'Anger': 0, 'Frustration': 0, 'Sadness': 0, 'Happiness': 0}
        cateStats = {'Neutral': 0, 'Anger': 0, 'Frustration': 0, 'Sadness': 0, 'Happiness': 0}
        for line in f:
            if (line[0] == "A"):
                if (wav_basename != ""):
                    # cateStats['Anger'] += cateStats['Frustration']
                    # cateStats['Frustration'] = 0

                    # determine if estimators have a common estimation
                    for category in categories:
                        # print("category", category, "cateStats[category]", cateStats[category])
                        # print("cateStats[category] / count", cateStats[category] / count)
                        if (cateStats[category] / count >= percentage):
                            wavFolder = re.search('(.*)_[^_]*', wav_basename).group(1)
                            wavFilePath = "{}/{}/{}.wav".format(wavDirPath, wavFolder, wav_basename)
                            placeUtteranceToFolder(wavFilePath, category, relativeSavePath)

                    # re-initialize
                    wav_basename = ""
                    count = 0
                    cateStats = {'Neutral': 0, 'Anger': 0, 'Frustration': 0, 'Sadness': 0, 'Happiness': 0}
                continue

            if (wav_basename == ""):
                regexp = re.compile(r'\[.*\].*(Ses[\d\w]*).*\[.*\]')
                result = regexp.search(line)
                if result:
                    wav_basename = result.group(1)
                # print(wav_basename)
                #                     print(line)
                else:
                    continue
            else:  # line with categories
                count += 1
                for category in categories:
                    if (re.search(category, line)):
                        cateStats[category] += 1


# print("category {} is counted as {}".format(category, cateStats[category]))
#                         print("category: ", category, line)

def getMelspectrogram(wavPath):
    if os.path.exists(wavPath) == False:
        print("Error, wavPath doesn't exist!")
        return
    (rate, sig) = wav.read(wavPath)
    # # Features: mel-spectrogram
    # features = librosa.feature.melspectrogram(y=sig, sr=rate, fmin=50, fmax=3000)

    if (sig.shape[0] / rate > 5) or (sig.shape[0] / rate < 2):
        return []

    features = librosa.feature.melspectrogram(y=sig, sr=rate, fmin=50, fmax=3000)
    features = scipy.misc.imresize(features, (features.shape[0], 300))

    features = features / np.max(features)

    # features = python_speech_features.mfcc(sig, rate)
    # features = np.transpose(features)

    # # Add padding
    # time_limit = 3000
    # if len(features[0]) < time_limit:
    #     arr = np.ones((13, time_limit - len(features[0])))
    #     arr = arr * np.average(features)
    #     features = np.concatenate((features, arr), axis=1)

    # print(features.shape)

    return features


def getFeature(wavPath):
    if os.path.exists(wavPath) == False:
        print("Error, wavPath doesn't exist!")
        return
    (rate, sig) = wav.read(wavPath)

    # #  - Mel Frequency Cepstral Coefficients
    # mfcc_feat = python_speech_features.mfcc(sig,rate)
    # d_mfcc_feat = python_speech_features.delta(mfcc_feat, 2)
    # # - Filterbank Energies
    # fbank_feat = python_speech_features.fbank(sig,rate)[0]
    # # - Log Filterbank Energies
    # logfbank_feat = python_speech_features.logfbank(sig,rate)
    # # - Spectral Subband Centroids
    # ssc_feat = python_speech_features.ssc(sig,rate)

    # Features: Log f bank
    # logfbank_feat = python_speech_features.logfbank(sig,rate)
    # delta_feat = python_speech_features.delta(logfbank_feat, 2)
    #
    # features = np.concatenate((logfbank_feat, delta_feat), axis = 1)

    # # Features: MFCC
    # features = python_speech_features.mfcc(sig, rate)

    # # Features: pyAudioAnalysis 34 features (Zero Crossing Rate, Energy, Spectral Centroid, MFCC, etc)
    # win = 0.025
    # step = 0.010
    # features = audioFeatureExtraction.stFeatureExtraction(sig, rate, int(win * rate), int(step * rate), )
    # features = np.transpose(features)

    # Features: pyAudioAnalysis 34 features and delta (68 in total)
    win = 0.025
    step = 0.010
    features = audioFeatureExtraction.stFeatureExtraction(sig, rate, int(win * rate), int(step * rate), )
    features = np.transpose(features)
    delta_features = python_speech_features.delta(features, 2)
    features = np.concatenate((features, delta_features), axis=1)

    # # Features: mel-spectrogram
    # features = librosa.feature.melspectrogram(y=sig, sr=rate, fmin=50, fmax=3000)
    # # Add padding
    # time_limit = 1500
    # if len(features[0]) < time_limit:
    #     arr = np.ones((128, time_limit - len(features[0])))
    #     arr = arr * np.average(features)
    #     features = np.concatenate((features, arr), axis=1)

    # print(features.shape)
    return features


def conv2D_AvePool(wavPath, kernalSize):
    input = getFeature(wavPath)
    (h, w) = input.shape
    input_tensor = input.reshape((1, h, w, 1))
    kernalResolution = (24, w)  # temporal resolutions: 16, 24, 32

    # build model
    inputs = Input(shape=(h, w, 1))
    x = Conv2D(kernalSize, kernalResolution,
               kernel_initializer=initializers.RandomNormal(mean=0.0, stddev=0.05, seed=123))(inputs)

    # model = Model(inputs=inputs, outputs=x)
    # result = model.predict(input_tensor)
    # # print(result.shape)

    output = AveragePooling2D((h - kernalResolution[0] + 1, 1))(x)
    model = Model(inputs=inputs, outputs=output)
    result = model.predict(input_tensor)[0, 0, 0, :]

    return result


def avePool(wavPath):
    input = getFeature(wavPath)
    (h, w) = input.shape
    input_tensor = input.reshape((1, h, w, 1))

    # build model
    inputs = Input(shape=(h, w, 1))

    output = AveragePooling2D((h, 1))(inputs)
    model = Model(inputs=inputs, outputs=output)
    # result = model.predict(input_tensor)
    # print(result.shape)
    result = model.predict(input_tensor)[0, 0, :, 0]
    # print(result.shape)
    # print(result)
    return result


def calculate_XY(wavDirBase, categories, kernalSize, numOfWavsForEachCategory=-1, architecture=0):
    counter = 0

    #     #waveArr = list(os.walk(wavDirBase))
    #     waveArr0 = [os.listdir(os.path.join(wavDirBase, x)) for x in os.listdir(wavDirBase) if not os.path.isfile(x)]
    #     fileCount = sum([len(list1) for list1 in waveArr0])
    #     # waveArr = [item for sublist in waveArr0 for item in sublist]

    x_all_list = []
    y_all_list = []

    print("Start processing at {}".format(datetime.datetime.utcnow()))
    for category in categories:
        waveArr = os.listdir(os.path.join(wavDirBase, category))
        numOfWavs = 0
        print("len(waveArr)", len(waveArr))
        for wavFile in waveArr:
            if wavFile.endswith(".wav") == False:
                continue

            wavPath = "{}/{}/{}".format(wavDirBase, category, wavFile)

            if architecture in [0, 1, 3]:
                # Use AvePool
                result = avePool(wavPath)
            elif architecture == 2:
                # Use conv2DAvePool
                result = conv2D_AvePool(wavPath, kernalSize)
            elif architecture == 4:
                result = getMelspectrogram(wavPath)
                print("result", result)

            if len(result)==0:
                continue

            # print("result.shape", result.shape)
            # print("x_all_list.append(result)", x_all_list.append(result))
            x_all_list.append(result)
            y_all_list.append(categories.index(category))

            # print("len(x_all_list)", len(x_all_list))

            counter += 1
            numOfWavs += 1

            if (numOfWavsForEachCategory > 0 and numOfWavs >= numOfWavsForEachCategory):
                break

            if (counter % 100 == 0):
                K.clear_session()
                print("{} files have been processed at {}".format(counter, datetime.datetime.utcnow()))
                #             if (counter>=200):
                #                 break;
                #             break

    x_all = np.array(x_all_list)
    y_all = np.array(y_all_list)

    print("x_all.shape", x_all.shape)
    print("y_all.shape", y_all.shape)

    return x_all, y_all
