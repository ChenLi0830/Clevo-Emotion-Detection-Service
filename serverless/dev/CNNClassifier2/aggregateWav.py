import os
from api import readFileAndAggregateUtterance

wavDir = "EmotionRecognization/wav"
emoTagsDir = "EmotionRecognization/emotionTags"

for emoFile in os.listdir(emoTagsDir):
    emoFilePath = "{}/{}".format(emoTagsDir, emoFile)
    readFileAndAggregateUtterance(emoFilePath, wavDir, "Preproc", percentage=0.66)

