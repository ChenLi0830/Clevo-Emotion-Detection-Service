import matplotlib.pyplot as plt
import numpy as np

import api
import librosa
import librosa.display
import scipy.io.wavfile as wav

import matplotlib.pyplot as plt
import scipy
import os
from keras.preprocessing.image import ImageDataGenerator

# x = np.linspace(0, 2, 100)
#
# plt.clf()
#
# plt.plot(range(len(x)), x, label='linear')
# plt.legend()

# plt.show()


features = api.getFeature("Preproc/Anger/Ses01F_impro05_F025.wav")

# print(features)

features = np.transpose(features)
print("features.shape", features.shape)

plt.clf()

# for i in range(len(features[:, 0])):
for i in range(6):
    # if np.average(features[i]) < -5:
    #     continue
    plt.plot(range(len(features[i])), features[i], label='feature: {}'.format(i))
plt.legend()

# plt.plot(range(len(features[0])), features[0], label='linear')

# (rate, sig) = wav.read("Preproc/Anger/Ses01F_impro05_F025.wav")


(rate, sig) = wav.read("Preproc/Anger/Ses01F_impro05_F009.wav")



# (rate, sig) = wav.read("Preproc/Anger/Ses01F_script03_2_F040.wav")
# (rate, sig) = wav.read("Preproc/Happiness/Ses01F_script01_3_F021.wav")


plt.clf()
# plt.figure(figsize=(10, 4))
S = librosa.feature.melspectrogram(y=sig, sr=rate, fmin=50, fmax=3000)
S_DB = librosa.power_to_db(S, ref=np.max)

# Generate more data
# datagen = ImageDataGenerator(width_shift_range=0.2, zoom_range=0.2)

# Load data
x_all = np.load("IEMOCAP_X.npy")
y_all = np.load("IEMOCAP_Y.npy")

datagen = ImageDataGenerator(width_shift_range=0.1,
                             zoom_range=[0.95, 1.05],
                             height_shift_range=0.1)

x_all = x_all[0:3, :, :]
y_all = y_all[0:3]

x_all_concat = x_all.reshape(-1, x_all.shape[1], x_all.shape[2], 1)
y_all_concat = y_all.reshape(-1, 1)

x_all_generated = []
y_all_generated = []

generateSize = x_all.shape[0] * 2
i = 0
for batch in datagen.flow(x=x_all_concat, y=y_all_concat, batch_size=2, save_to_dir=None):
    i += 1
    print("i", i)
    # print("batch", batch)
    # x_batch = print("batch[0].shape", batch[0].shape)
    x_batch = batch[0]
    print("x_batch.shape", x_batch.shape)
    y_batch = batch[1]
    print("y_batch.shape", y_batch.shape)
    # x_batch = batch[0][0, :, :, 0]
    # y = batch[1]
    # print("batch[1].shape", batch[1].shape)
    # print("batch.shape", batch.shape)

    for j in range(x_batch.shape[0]):
        print("j", j)
        print("x_batch[j, :, :, 0].shape", x_batch[j, :, :, 0].shape)
        plt.figure()
        x_all_generated.append(x_batch[j, :, :, 0])
        y_all_generated.append(y_batch[j, 0])
        # # librosa.display.specshow(S, y_axis='mel', x_axis='time', fmin=50, fmax=3000)
        # librosa.display.specshow(x_batch[j, :, :, 0], y_axis='mel', x_axis='time', fmin=50, fmax=3000)
        # plt.colorbar()
        # plt.title("generated S_DB: {}/{}".format(i, j))
    # plt.figure()
    # # librosa.display.specshow(S, y_axis='mel', x_axis='time', fmin=50, fmax=3000)
    # librosa.display.specshow(x, y_axis='mel', x_axis='time', fmin=50, fmax=3000)
    # plt.colorbar()
    # plt.title("generated S_DB: {}".format(i))
    if i > generateSize:
        break  # otherwise the generator would loop indefinitely

x_all_generated = np.array(x_all_generated).reshape(-1, x_all_generated.shape[1], x_all_generated.shape[2], 1)
# x_all_generated = x_all_generated.reshape(-1, x_all_generated.shape[1], x_all_generated.shape[2], 1)
y_all_generated = np.array(y_all_generated).reshape(-1, 1)
# y_all_generated.reshape(-1, 1)
print("x_all_generated.shape", x_all_generated.shape)
print("y_all_generated.shape", y_all_generated.shape)

for j in range(x_all_generated.shape[0]):
    # librosa.display.specshow(S, y_axis='mel', x_axis='time', fmin=50, fmax=3000)
    plt.figure()
    librosa.display.specshow(x_all_generated[j, :, :, 0], y_axis='mel', x_axis='time', fmin=50, fmax=3000)
    plt.colorbar()
    plt.title("generated S_DB: {}/{}".format(i, j))


test = S_DB.reshape(1, S_DB.shape[0], S_DB.shape[1], 1)
y_test = np.array([1]).reshape(1, 1)
plt.figure()
# librosa.display.specshow(S, y_axis='mel', x_axis='time', fmin=50, fmax=3000)
librosa.display.specshow(S_DB, y_axis='mel', x_axis='time', fmin=50, fmax=3000)
plt.colorbar()
plt.title("original S_DB")
i = 0
for batch in datagen.flow(x=test, y=y_test, batch_size=1, save_to_dir=None):
    i += 1
    # print("batch", batch)
    print("batch[0].shape", batch[0].shape)
    x = batch[0][0, :, :, 0]
    y = batch[1]
    print("batch[1].shape", batch[1].shape)
    # print("batch.shape", batch.shape)

    plt.figure()
    # librosa.display.specshow(S, y_axis='mel', x_axis='time', fmin=50, fmax=3000)
    librosa.display.specshow(x, y_axis='mel', x_axis='time', fmin=50, fmax=3000)
    plt.colorbar()
    plt.title("generated S_DB: {}".format(i))
    if i > 5:
        break  # otherwise the generator would loop indefinitely

print("S.shape", S.shape)

plt.figure()
# librosa.display.specshow(S, y_axis='mel', x_axis='time', fmin=50, fmax=3000)
librosa.display.specshow(S_DB, y_axis='mel', x_axis='time', fmin=50, fmax=3000)
plt.colorbar()

# S2 = scipy.misc.imresize(S, 0.25)
S2 = scipy.misc.imresize(S, (S.shape[0], 300))
plt.figure()
librosa.display.specshow(S2, y_axis='mel', x_axis='time', fmin=50, fmax=3000)

S2 = S2 / np.max(S2)

plt.colorbar()
# librosa.display.specshow(librosa.power_to_db(S,ref=np.max), y_axis='mel', x_axis='time', fmin=50, fmax=3000)




wavDirBase = "Preproc"
category = "AngerP"
waveArr = os.listdir(os.path.join(wavDirBase, category))
count = 0
for wavFile in waveArr:
    if (count >= 12):
        break
    if wavFile.endswith(".wav") == False:
        continue
    wavPath = "{}/{}/{}".format(wavDirBase, category, wavFile)
    (rate, sig) = wav.read(wavPath)

    # if (len(sig)/rate < 2) or (len(sig)/rate > 3):
    #     continue

    S = librosa.feature.melspectrogram(y=sig, sr=rate, fmin=50, fmax=3000)
    print("S.shape", S.shape)

    if count % 4 == 0:
        plt.figure()
    plt.subplot(2, 2, count % 4 + 1)
    librosa.display.specshow(S, y_axis='mel', x_axis='time', fmin=50, fmax=3000)
    plt.title(wavFile)
    # plt.colorbar()
    count += 1



# np.average(S)
time_limit = 1500
if len(S[0]) < time_limit:
    arr = np.ones((128, time_limit - len(S[0])))
    arr = arr * np.average(S)
    S = np.concatenate((S, arr), axis=1)

librosa.display.specshow(S, y_axis='mel', x_axis='time', fmin=50, fmax=3000)

import python_speech_features
features = python_speech_features.mfcc(sig, rate)
features = np.transpose(features)

features = np.mean(features, axis=1)

plt.clf()
plt.imshow(features, aspect='auto')
plt.colorbar()
