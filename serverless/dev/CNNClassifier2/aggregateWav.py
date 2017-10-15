import os
from api import readFileAndAggregateUtterance

wavDir = "/Users/Chen/百度云同步盘/Startup/Clevo/数据/IEMOCAP_full_release/EmotionRecognization/wav"
emoTagsDir = "/Users/Chen/百度云同步盘/Startup/Clevo/数据/IEMOCAP_full_release/EmotionRecognization/emotionTags"

for emoFile in os.listdir(emoTagsDir):
    emoFilePath = "{}/{}".format(emoTagsDir, emoFile)
    readFileAndAggregateUtterance(emoFilePath, wavDir, "Preproc", percentage=0.66)

