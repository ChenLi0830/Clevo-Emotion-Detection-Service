import os
from scipy.io import wavfile
import json
import ast
import numpy as np

jsonDirPath = '/Users/Chen/百度云同步盘/Startup/Clevo/联动数据/emotionJson/'
wavDirPath = '/Users/Chen/百度云同步盘/Startup/Clevo/联动数据/wav/'
wavSavePath = '/Users/Chen/百度云同步盘/Startup/Clevo/联动数据/wavSegs/'

if (os.path.isdir(jsonDirPath) != True):
    raise ValueError('jsonDirPath is not a dir')
if (os.path.isdir(wavDirPath) != True):
    raise ValueError('wavDirPath is not a dir')
if (os.path.isdir(wavSavePath) != True):
    raise ValueError('wavSavePath is not a dir')

jsonArr = os.listdir(jsonDirPath)
wavArr = os.listdir(wavDirPath)
print(len(jsonArr))
print(len(wavArr))

# for i,fileName in enumerate(wavArr[1:2]):
for i, fileName in enumerate(wavArr):
    print(i, fileName)
    filePath = wavDirPath + fileName
    print("filePath", filePath)
    [sampleRate, audio] = wavfile.read(filePath)
    print(audio.shape[0])
    #     print(sampleRate)
    start = 0
    duration = 10 * sampleRate
    step = 5 * sampleRate
    index = 0
    while start + duration < audio.shape[0]:
        audioSeg = audio[start:start + duration]
        #         print(audioSeg.shape[0])
        if (audioSeg.shape[0] == 80000):
            filePrefix = fileName.split('.')[0]
            newFilePath = wavSavePath + filePrefix + "__" + str(index) + ".wav"
            index += 1
            wavfile.write(newFilePath, sampleRate, np.array(audioSeg, dtype="int16"))

        start += step
