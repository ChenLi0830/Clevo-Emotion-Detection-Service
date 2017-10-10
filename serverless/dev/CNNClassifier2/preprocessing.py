import shutil
import re
import os
import numpy as np
import python_speech_features
import scipy.io.wavfile as wav
from keras import backend as K
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D, Input, AveragePooling2D
import datetime


def placeUtteranceToFolder(wavPath, category, savePath):
    catePath = savePath+"/"+category
    if (os.path.exists(wavPath)!=True):
        raise ValueError("wavPath doesn't exist")
    if (os.path.exists(savePath)!=True):
        print("Creating dir: " + savePath)
        os.makedirs(savePath)
    if (os.path.exists(catePath)!=True):
        print("Creating dir: " + catePath)
        os.makedirs(catePath)

    filename = os.path.basename(wavPath)

    shutil.copy2(wavPath, catePath) # complete target filename given

    print("{} is put into path: {}".format(filename, catePath))


def readFileAndAggregateUtterance(filePath, wavDir, relativeSavePath):
    categories = ['Neutral', 'Anger', 'Frustration', 'Sadness', 'Happiness']
    wavDirPath = "/Users/Chen/百度云同步盘/Startup/Clevo/数据/IEMOCAP_full_release/EmotionRecognization/wav/"

    with open(filePath) as f:
        wav_basename = ""
        count = 0
        cateStats = {'Neutral':0, 'Anger':0, 'Frustration':0, 'Sadness':0, 'Happiness':0}
        for line in f:
            if (line[0]=="A"):
                if (wav_basename != ""):
                    cateStats['Anger'] += cateStats['Frustration']
                    cateStats['Frustration'] = 0

#                     print("count", count)
                    # determine if estimators have a common estimation
                    for category in categories:
                        # print("category", category, "cateStats[category]", cateStats[category])
                        # print("cateStats[category] / count", cateStats[category] / count)
                        if (cateStats[category] / count > 0.5):
                            wavFolder = re.search('(.*)_[^_]*', wav_basename).group(1)
                            wavFilePath = "{}/{}/{}.wav".format(wavDirPath, wavFolder, wav_basename)
                            placeUtteranceToFolder(wavFilePath, category, relativeSavePath)

                    # re-initialize
                    wav_basename = ""
                    count = 0
                    cateStats = {'Neutral':0, 'Anger':0, 'Frustration':0, 'Sadness':0, 'Happiness':0}
                continue

            if (wav_basename == ""):
                regexp = re.compile(r'\[.*\].*(Ses[\d\w]*).*\[.*\]')
                result = regexp.search(line)
                if result:
                    wav_basename = result.group(1)
#                     print(wav_basename)
#                     print(line)
                else:
                    continue
            else: # line with categories
                count += 1
                for category in categories:
                    if (re.search(category, line)):
                        cateStats[category]+=1
#                         print("category {} is counted as {}".format(category, cateStats[category]))
#                         print("category: ", category, line)


def getFeature(wavPath):
    (rate,sig) = wav.read(wavPath)
    # features = []
    logfbank_feat = python_speech_features.logfbank(sig,rate)
    delta_feat = python_speech_features.delta(logfbank_feat, 2)

    features = np.concatenate((logfbank_feat, delta_feat), axis = 1)
#     print(features.shape)
    return features



def calculate_XY(wavDirBase, categories, kernalSize):
    counter = 0
    #waveArr = list(os.walk(wavDirBase))
    waveArr0 = [os.listdir(os.path.join(wavDirBase, x)) for x in os.listdir(wavDirBase) if not os.path.isfile(x)]
    fileCount = sum([len(list1) for list1 in waveArr0])
    # waveArr = [item for sublist in waveArr0 for item in sublist]
    print("total file count: ", fileCount)

    x_all_list = []
    y_all_list = []

    print("Start processing at {}".format(datetime.datetime.utcnow()))
    for category in categories:
        waveArr = os.listdir(os.path.join(wavDirBase, category))
        # print("len(waveArr)", len(waveArr))
        for wavFile in waveArr:

            wavPath = "{}/{}/{}".format(wavDirBase, category, wavFile)
            input = getFeature(wavPath)
            input_tensor = input.reshape((1,input.shape[0], input.shape[1] ,1))

            inputs = Input(shape=(input.shape[0], input.shape[1], 1))
            x = Conv2D(kernalSize, (25, 52))(inputs)
            x = AveragePooling2D((input.shape[0]-24, 1))(x)

            model = Model(inputs=inputs, outputs=x)
            result = model.predict(input_tensor)

            x_all_list.append(result[0,0,0,:])
            y_all_list.append(categories.index(category))

            counter += 1
            if (counter % 100 == 0):
                K.clear_session()
                print("{} files have been processed at {}".format(counter, datetime.datetime.utcnow()))
    #             if (counter>=200):
    #                 break;
            # break

    x_all = np.array(x_all_list)
    y_all = np.array(y_all_list)

    return x_all, y_all
