import shutil
import re
import os
import numpy as np
import python_speech_features
import scipy.io.wavfile as wav
from keras import initializers, backend as K
from keras.layers import Conv2D, MaxPooling2D, Input, AveragePooling2D
from keras import optimizers
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Activation, Conv2D, MaxPooling2D, BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint
import datetime
from pyAudioAnalysis import audioFeatureExtraction
import librosa
import librosa.display
import scipy
import config
from keras.preprocessing.image import ImageDataGenerator

def trainNetwork(X_train, Y_train_cat, X_valid, Y_valid_cat, X_test, Y_test_cat, architecture, num_classes, kernalSize,
                 batch_size, epochs, class_weight_dict):

    # Build modal
    if architecture == 0:
        lastModel = Sequential()
        lastModel.add(Dense(units=num_classes, input_dim=X_train.shape[1], activation='softmax'))
        lastModel.compile(loss='categorical_crossentropy',
                          # optimizer=adam,
                          # optimizer='rmsprop',
                          optimizer='adam',
                          metrics=['accuracy'])

    elif architecture == 1:
        lastModel = Sequential()
        print("x_all.shape[1]", X_train.shape[1])
        lastModel.add(Dense(units=8, input_dim=X_train.shape[1], activation='relu'))
        lastModel.add(Dense(units=4, activation='relu'))
        # lastModel.add(Dense(units=4, input_dim=4))
        # lastModel.add(Dense(units=8, input_dim=8))
        lastModel.add(Dense(units=num_classes, activation='softmax'))
        # lastModel.add(Activation('softmax'))
        # print()
        lastModel.compile(loss='categorical_crossentropy',
                          # optimizer=adam,
                          # optimizer='rmsprop',
                          optimizer='adam',
                          metrics=['accuracy'])

    elif architecture == 2:
        lastModel = Sequential()
        lastModel.add(Dense(units=num_classes, input_dim=kernalSize))
        # lastModel.add(Dense(units=512, input_dim=kernalSize))
        # lastModel.add(Dense(units=num_classes, input_dim=512))
        lastModel.add(Activation('softmax'))
        # lastModel.add(Dense(10, activation='softmax'))

        # sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        # adam = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

        lastModel.compile(loss='categorical_crossentropy',
                          # optimizer=adam,
                          optimizer='rmsprop',
                          # optimizer='adam',
                          metrics=['accuracy'])

    elif architecture == 3:
        lastModel = Sequential()
        print("x_all.shape[1]", X_train.shape[1])
        lastModel.add(Dense(units=32, input_dim=X_train.shape[1], activation='relu'))
        lastModel.add(Dense(units=16, activation='relu'))
        lastModel.add(Dense(units=8, activation='relu'))
        # lastModel.add(Dense(units=4, input_dim=4))
        # lastModel.add(Dense(units=8, input_dim=8))
        lastModel.add(Dense(units=num_classes, activation='softmax'))
        # lastModel.add(Activation('softmax'))
        # print()
        lastModel.compile(loss='categorical_crossentropy',
                          # optimizer=adam,
                          # optimizer='rmsprop',
                          optimizer='adam',
                          metrics=['accuracy'])

    elif architecture == 4:
        lastModel = Sequential()
        # print("x_all.shape[1]", X_train.shape[1])
        # x_all.reshape(-1, 128, 1500, 1)

        # lastModel.add(Conv2D(64, (3, 3), padding="same"))
        # lastModel.add(Activation('relu'))
        # lastModel.add(MaxPooling2D(pool_size=(2, 2), padding="same"))

        lastModel.add(Conv2D(32, (3, 3), input_shape=(X_train[0].shape[0], X_train[0].shape[1], 1), padding="same"))
        lastModel.add(MaxPooling2D(pool_size=(2, 2), padding="same"))
        lastModel.add(BatchNormalization(axis=3))
        lastModel.add(Activation('relu'))

        lastModel.add(Conv2D(32, (3, 3), padding="same"))
        lastModel.add(MaxPooling2D(pool_size=(2, 2), padding="same"))
        lastModel.add(BatchNormalization(axis=3))
        lastModel.add(Activation('relu'))

        lastModel.add(Conv2D(64, (3, 3), padding="same"))
        lastModel.add(MaxPooling2D(pool_size=(2, 2), padding="same"))
        lastModel.add(BatchNormalization(axis=3))
        lastModel.add(Activation('relu'))

        lastModel.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
        lastModel.add(Dense(128))
        lastModel.add(Activation('relu'))
        lastModel.add(BatchNormalization())
        lastModel.add(Dropout(0.5))
        lastModel.add(Dense(units=num_classes, activation='softmax'))

        lastModel.compile(loss='categorical_crossentropy',
                          # optimizer=adam,
                          # optimizer='rmsprop',
                          optimizer='adam',
                          metrics=['accuracy'])


    # callbacks
    esCallback = EarlyStopping(monitor='val_loss',
                               min_delta=0,
                               patience=10,
                               verbose=1, mode='auto')

    saveModelFilePath = "savedModel"
    if os.path.exists(saveModelFilePath) != True:
        print("Creating dir: " + saveModelFilePath)
        os.makedirs(saveModelFilePath)

    savedModelPath = saveModelFilePath + "/weights.best.hdf5"

    checkpoint = ModelCheckpoint(savedModelPath, monitor='val_loss', verbose=1, save_best_only=True,
                                 save_weights_only=False,
                                 mode='auto', period=1)

    # fit model
    lastModel.fit(X_train, Y_train_cat, batch_size=batch_size, epochs=epochs, verbose=1,
                  validation_data=(X_valid, Y_valid_cat), class_weight=class_weight_dict,
                  callbacks=[checkpoint, esCallback])

    print("Loading best model weight...")
    lastModel.load_weights(savedModelPath)
    # Test modal
    score = lastModel.evaluate(X_test, Y_test_cat, verbose=0)
    unweightedLoss = score[0]
    unweightedAcc = score[1]
    print('Test loss:', unweightedLoss)
    print('Test Unweighted accuracy:', unweightedAcc)

    # y_pred = lastModel.predict(X_test)
    # acc = sum([np.argmax(Y_test_cat[i])==np.argmax(y_pred[i]) for i in range(len(X_test))])/len(X_test)
    # print('Real test accuracy:', acc)
    y_pred = lastModel.predict(X_test)
    weightedAccuracyArr = np.zeros(num_classes)
    count = np.zeros(num_classes)
    for i in range(len(X_test)):
        categoryIdx = np.argmax(Y_test_cat[i])
        weightedAccuracyArr[categoryIdx] += np.argmax(Y_test_cat[i]) == np.argmax(y_pred[i])
        count[categoryIdx] += 1

    weightedAccuracyArr = weightedAccuracyArr / count
    weightedAcc = sum(weightedAccuracyArr) / num_classes

    print("Weighted category counts", count)
    print("WeightedAccuracyArr", weightedAccuracyArr)
    print("Weighted Accuracy: ", weightedAcc)

    # Save modal
    lastModel.save('emotion_model.h5')  # creates a HDF5 file 'my_model.h5'
    lastModel.save_weights('emotion_model_weights.h5')

    return unweightedAcc, weightedAcc

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
    categories = config.arc1Config['categories']

    with open(filePath) as f:
        wav_basename = ""
        count = 0
        # cateStats = {'Neutral': 0, 'Anger': 0, 'Frustration': 0, 'Sadness': 0, 'Happiness': 0}
        cateStats = dict([(category, 0) for category in categories])
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
                            wavFilePath = "{}/{}/{}.wav".format(wavDir, wavFolder, wav_basename)
                            placeUtteranceToFolder(wavFilePath, category, relativeSavePath)

                    # re-initialize
                    wav_basename = ""
                    count = 0
                    cateStats = dict([(category, 0) for category in categories])
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


def generateData(x, y, batch_size=4, width_shift_range=0.2, zoom_range=0.05):
    datagen = ImageDataGenerator(width_shift_range=width_shift_range, zoom_range=zoom_range)

    # x_all.shape
    # y_all.shape

    x = x.reshape(-1, x.shape[1], x.shape[2], 1)
    y = y.reshape(-1, 1)

    x_generated = []
    y_generated = []

    # generateSize = x_all.shape[0] * 2
    i = 0
    print("Generating data")
    for batch in datagen.flow(x=x, y=y, batch_size=batch_size, save_to_dir=None):
        i += 1
        # print("batch", batch)
        # x_batch = print("batch[0].shape", batch[0].shape)
        x_batch = batch[0]
        # print("x_batch.shape", x_batch.shape)
        y_batch = batch[1]
        # print("y_batch.shape", y_batch.shape)

        for j in range(x_batch.shape[0]):
            # print("j", j)
            # print("x_batch[j, :, :, 0].shape", x_batch[j, :, :, 0].shape)
            x_generated.append(x_batch[j, :, :, 0])
            y_generated.append(y_batch[j, 0])
        if i > x.shape[0]:
            break  # otherwise the generator would loop indefinitely

    x_generated = np.array(x_generated)
    # x_all_generated = x_all_generated.reshape(-1, x_all_generated.shape[1], x_all_generated.shape[2], 1)
    y_generated = np.array(y_generated)
    # y_all_generated = y_all_generated.reshape(-1, 1)
    return x_generated, y_generated
    # x_all = x_generated
    # y_all = y_generated


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
                # print("result", result)

            if len(result) == 0:
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
