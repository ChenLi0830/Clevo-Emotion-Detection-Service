import os
from api import readFileAndAggregateUtterance

wavDir = "raw_data/EmotionRecognization/wav"
emoTagsDir = "raw_data/EmotionRecognization/emotionTags"

for emoFile in os.listdir(emoTagsDir):
    emoFilePath = "{}/{}".format(emoTagsDir, emoFile)
    readFileAndAggregateUtterance(emoFilePath, wavDir, "Preproc", percentage=0.66)

