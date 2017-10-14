import matplotlib.pyplot as plt
import numpy as np

import api
import librosa
import librosa.display
import scipy.io.wavfile as wav

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
# (rate, sig) = wav.read("Preproc/Anger/Ses01F_script03_2_F040.wav")
(rate, sig) = wav.read("Preproc/Happiness/Ses01F_script01_3_F021.wav")


import matplotlib.pyplot as plt

plt.clf()
# plt.figure(figsize=(10, 4))
S = librosa.feature.melspectrogram(y=sig, sr=rate, fmin=50, fmax=3000)
print("S.shape", S.shape)
# librosa.display.specshow(librosa.power_to_db(S,ref=np.max), y_axis='mel', x_axis='time', fmin=50, fmax=3000)
librosa.display.specshow(S, y_axis='mel', x_axis='time', fmin=50, fmax=3000)
plt.colorbar()

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

plt.clf()
plt.imshow(features, aspect='auto')
plt.colorbar()
