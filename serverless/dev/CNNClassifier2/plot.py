import matplotlib.pyplot as plt
import numpy as np

import api
import librosa
import librosa.display
import scipy.io.wavfile as wav

import matplotlib.pyplot as plt
import scipy
import os

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


(rate, sig) = wav.read("Preproc/Anger/Ses01F_impro01_M008.wav")



# (rate, sig) = wav.read("Preproc/Anger/Ses01F_script03_2_F040.wav")
# (rate, sig) = wav.read("Preproc/Happiness/Ses01F_script01_3_F021.wav")


plt.clf()
# plt.figure(figsize=(10, 4))
S = librosa.feature.melspectrogram(y=sig, sr=rate, fmin=50, fmax=3000)
print("S.shape", S.shape)

plt.figure()
librosa.display.specshow(S, y_axis='mel', x_axis='time', fmin=50, fmax=3000)
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
