import os
from scipy.io import wavfile
import json
import ast
import numpy as np

jsonDirPath = '/Users/Chen/百度云同步盘/Startup/Clevo/联动数据/emotionJson/'
wavDirPath = '/Users/Chen/百度云同步盘/Startup/Clevo/联动数据/wav/'

if (os.path.isdir(jsonDirPath)!=True):
    raise ValueError('jsonDirPath is not a dir')
if (os.path.isdir(wavDirPath)!=True):
    raise ValueError('wavDirPath is not a dir')



import requests 
requests.packages.urllib3.disable_warnings()
import json

def getAnalysis(API_Key,WavPath):
    res = requests.post("https://token.beyondverbal.com/token",data={"grant_type":"client_credentials","apiKey":API_Key})
    token = res.json()['access_token']
    headers={"Authorization":"Bearer "+token}
    pp = requests.post("https://apiv4.beyondverbal.com/v3/recording/start",json={"dataFormat": { "type":"WAV" }},verify=False,headers=headers)
    if pp.status_code != 200:
        print(pp.status_code, pp.content)
        return
    recordingId = pp.json()['recordingId']
    with open(WavPath,'rb') as wavdata:
        r = requests.post("https://apiv4.beyondverbal.com/v3/recording/"+recordingId,data=wavdata, verify=False, headers=headers)
        return r.json()
    
# Test    
# 4a34bb65-5bfd-4006-af26-64aa63055b8b
# res = getAnalysis("4a34bb65-5bfd-4006-af26-64aa63055b8b", wavDirPath+wavArr[0])
# print(json.dumps(res))
# res = getAnalysis("ee1e2100-52f3-49aa-896c-ac56cd62a5c1","data/wave/642/test.wav")
#print json.dumps(res)


# from os.path import basename
import os

for f in wavArr:
    basename = os.path.basename(f)
    baseWithoutExtension = os.path.splitext(basename)[0]

    if baseWithoutExtension + ".json" in jsonArr:
        print(baseWithoutExtension + ".json exist already")
    else:
        print("creating emotion json file for: " + f)
        
        res = getAnalysis("4a34bb65-5bfd-4006-af26-64aa63055b8b",wavDirPath + basename)        
#         res = getAnalysis("ee1e2100-52f3-49aa-896c-ac56cd62a5c1",wavDirPath + basename)
        if res!=None and len(str(res))>1000:
            with open(jsonDirPath + baseWithoutExtension + ".json", 'w') as outfile:
                json.dump(res, outfile)
                print("successfully created" + jsonDirPath + baseWithoutExtension + ".json")
        else:
            print("Can't get more emotion Json files, breaking the loop")
            break


