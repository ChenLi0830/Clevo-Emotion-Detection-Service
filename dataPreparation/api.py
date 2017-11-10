import os
from scipy.io import wavfile

import numpy as np
from array_split import shape_split

# jsonDirPath = '/Users/Chen/百度云同步盘/Startup/Clevo/联动数据/emotionJson/'
# wavDirPath = '/Users/Chen/百度云同步盘/Startup/Clevo/联动数据/wav/'
# wavSavePath = '/Users/Chen/百度云同步盘/Startup/Clevo/联动数据/wavSegs/'
#
# if (os.path.isdir(jsonDirPath) != True):
#     raise ValueError('jsonDirPath is not a dir')
# if (os.path.isdir(wavDirPath) != True):
#     raise ValueError('wavDirPath is not a dir')
# if (os.path.isdir(wavSavePath) != True):
#     raise ValueError('wavSavePath is not a dir')
#
# jsonArr = os.listdir(jsonDirPath)
# wavArr = os.listdir(wavDirPath)
# print(len(jsonArr))
# print(len(wavArr))

#
# jsonArr = [{"bg":"410","ed":"4010","onebest":"您好！966为您服务，请问有什么能帮您的吗？","speaker":"1"},{"bg":"4250","ed":"17210","onebest":"你好，我什么业务也没定，刚才你们怎么给我发信息说我有个小格子数，呢因为你们出现这个信息的时候我就给翻了，根本我就没点播，说我有一个那个下载一个什么功能。","speaker":"2"},{"bg":"17240","ed":"23680","onebest":"啊是您是您来电的13841314049这个手机号扣费了吗？","speaker":"1"},{"bg":"23700","ed":"28330","onebest":"啊对，啊我不我刚才我在微信上我没记这个业务。啊。","speaker":"2"},{"bg":"28550","ed":"31320","onebest":"您稍等帮您进行查询，","speaker":"1"},{"bg":"31550","ed":"32250","onebest":"然后","speaker":"1"},{"bg":"43090","ed":"47060","onebest":"帅女士正在帮您查询。","speaker":"1"},{"bg":"47450","ed":"48760","onebest":"唉好。","speaker":"2"},{"bg":"51100","ed":"51800","onebest":"嗯","speaker":"1"},{"bg":"66100","ed":"68370","onebest":"一号女士感谢耐心短暂。","speaker":"1"},{"bg":"68390","ed":"87880","onebest":"查询到您这个在9:51的时候购买，直接9:51点出来可能欢乐斗地主，因为我都没见过你，你那个亲戚都说确认我，但但是我现在都没信任我，直接就给删除删除。它反出来了很多信息我都不删除，我没承认它怎么就能叫我支付了你。","speaker":"2"},{"bg":"88170","ed":"96900","onebest":"我们这边查询到您确实有这个回复短信如果我就没回复，我给你做，你哪里胖就自动焊吗？","speaker":"1"},{"bg":"97580","ed":"98770","onebest":"你说。","speaker":"2"},{"bg":"98790","ed":"120520","onebest":"嗯因为查询到确实有这个回复短信如果您说不是您本人的回复的话，可能是您不小心点到这个什么扣费软件或者说手机中病毒了。如果您想避免以后再出现这个类似的情况，可以给您进行一个免费的号码保护，以后您手机中病毒也不会和您话费的给您关闭支付通道您需要吗？","speaker":"1"},{"bg":"121240","ed":"134350","onebest":"你这个师傅现在你必须给我灌输，因为我没有这些，因为我从来不定这些业务，他一个你这个要是靠我20块钱话费我肯定不干，因为什么你这个进来之后我干事我都没确认，我直接就删除了","speaker":"2"},{"bg":"134840","ed":"160680","onebest":"女士这个您支付的只有十元。没有20年的时候这里人写的是秘密客户1086发过来的，说真的客户你好，于2014年6月39点51分点播了中国移动互联网公司提供的欢乐斗地主什么35万什么经济业务，话费是20元，我都没有支付，这些东西啊我干事我都没有选择呀。","speaker":"2"},{"bg":"160800","ed":"174550","onebest":"女士，您这个点播扣费只扣了10元2十分20元那个费用没有扣除成功，如果您不相信的话可以查询一下您的话费余额好吧，你你这个自愿你也不应该给我，因为我没选择，呀","speaker":"1"},{"bg":"174690","ed":"202520","onebest":"于是这个不是我们给您扣除的话费，这是您捡到商家扣的，我们这边只是支付通道，如果您表示不是您本人操作的可以给您进行反馈，然后到时候咱们3到5工作日让商家主动联系您，您跟商家进行协商是给您退费处理还是怎么的好吧，要不我我就找那个移动公司去，因为你们这你给我开出那个是不出卖了什么你我看我本人都不知道，因为我从来不信这些业务，","speaker":"1"},{"bg":"203000","ed":"217520","onebest":"女士，您这个支付通道是这个入网时间足够之后他自动开通的这个传统，但是我干脆我没定位业务，那你这么你你不是那个叫我不明白社会，嘛因为我都不知道那为啥，把我的钱就扣出去了。","speaker":"2"},{"bg":"217620","ed":"233370","onebest":"于是跟您说了给您反馈，然后到时候3到5工作日让商家联系您您跟商家协商是给您进行退费处理，或者说其他的您跟商家协商好吧行我不行，我觉得还得我还得找移动公司，","speaker":"1"},{"bg":"233400","ed":"255140","onebest":"那如果您不放心的话找移动公司也可以让移动公司联系我们，那您还需要我帮你进行反馈吗？你说你先给我反馈，嘛因为这个电话是移动公司给我的好的，那我这边给您进行反馈，还有其他能帮您的吗？到时候电话我那个字你把我那个是通报给我关了我我不知处","speaker":"1"},{"bg":"255160","ed":"262340","onebest":"已经给您关闭了联系电话联系您是联系您来电的13841314049手机号吗？","speaker":"1"},{"bg":"262360","ed":"267600","onebest":"对，就是这个号码，嗯你要发行结果反馈，还有其他人办理了吗？","speaker":"1"},{"bg":"267610","ed":"271880","onebest":"没有了。嗯感谢您的来电，请您稍后评价，再见。","speaker":"1"}]
# path = "20170630103142_966_13841314049_601.wav"
jsonArr = [{"bg":"180","ed":"3620","onebest":"你好，周六为您服务，请问什么可以帮你？","speaker":"1"},{"bg":"4080","ed":"11950","onebest":"唉你好，那个我想问一下我这个课堂有一个15块钱的支付那个脉动是吧？","speaker":"2"},{"bg":"11970","ed":"16860","onebest":"我不知道，我跟你帮我查一下是来电，这个11的手机号码嘛。","speaker":"1"},{"bg":"17820","ed":"22120","onebest":"嗯来电这个手机号码吗？","speaker":"2"},{"bg":"22230","ed":"42270","onebest":"对对对有钱烧的我这边帮您看一下您好先生抱歉让您久等了我这边看到6月19份6月19号一共有两笔交易一笔成功的1:4兆的成功的这里是一个常州A图A图游戏15元礼包这个是按次点播的游戏你点过一次收一次费用不点拨不收取任何费用的","speaker":"1"},{"bg":"42810","ed":"72600","onebest":"这个是属于咱们我的我我无意当中点的，我觉得本身属于暗示点拨的游戏，如果你以后不想再产生相应费用的话，我这边可以给你手机号码对一下号码保护处理。如果通过我是平台就是话费再也不能购买任何游戏上面应该需要做保护吗先生那你除了保护之外能把这四块钱能够对未来不这个抱歉真的15块钱在当时都已经支付成功了，我能做的话就是您说一下照顾bb","speaker":"1"},{"bg":"72610","ed":"76320","onebest":"以后再产生类似扣费你还需要做保护吗？","speaker":"1"},{"bg":"76500","ed":"91820","onebest":"那我找10086还能能够对我来说这个抱歉，这个是你那个是按次点播的游行点播一次收一次费用，不点拨不出去了，费用我这个也不知道，我这边只能给你说一下保护，避免以后再产生类似的口碑","speaker":"1"},{"bg":"92160","ed":"98620","onebest":"好的你拿着礼物帮我宝贝原来已经把我好了，什么还有什么，其他能帮你把24小时等一下","speaker":"1"},{"bg":"98990","ed":"101390","onebest":"没有了就之前。","speaker":"1"}]
path = "20170623095248_956_15140969348_601.wav"

#
# # for i,fileName in enumerate(wavArr[1:2]):
# for i, fileName in enumerate(wavArr):
#     print(i, fileName)
#     filePath = wavDirPath + fileName
#     print("filePath", filePath)
#     [sampleRate, audio] = wavfile.read(filePath)
#     print(audio.shape[0])
#     #     print(sampleRate)
#     start = 0
#     duration = 10 * sampleRate
#     step = 5 * sampleRate
#     index = 0
#     while start + duration < audio.shape[0]:
#         audioSeg = audio[start:start + duration]
#         #         print(audioSeg.shape[0])
#         if (audioSeg.shape[0] == 80000):
#             filePrefix = fileName.split('.')[0]
#             newFilePath = wavSavePath + filePrefix + "__" + str(index) + ".wav"
#             index += 1
#             wavfile.write(newFilePath, sampleRate, np.array(audioSeg, dtype="int16"))
#
#         start += step
#

def segment_wav(jsonArr, path):
    if os.path.exists(path) != True:
        raise ValueError("audio path doesn't exist")
    # todo: check if it is .wav file
    [sampleRate, audio] = wavfile.read(path)
    print("sampleRate, len(audio)", sampleRate, len(audio))
    for i, json in enumerate(jsonArr):
        print(i, json)
        begin = int(int(json['bg']) * sampleRate / 1000)
        end = int(int(json['ed']) * sampleRate / 1000)
        audioSeg = audio[begin:end]
        filePrefix = os.path.basename(path).split('.')[0]
        savePath = "save"
        if os.path.isdir(savePath) != True:
            os.makedirs(savePath)
        newFilePath = "{}/{}__{}.wav".format(savePath, filePrefix, str(i))
        wavfile.write(newFilePath, sampleRate, np.array(audioSeg, dtype="int16"))
    # return []

def segment_wav_may(jsonArr, file_path, savePath='save', low_th=3, high_th=6):
    if os.path.exists(file_path) != True:
        raise ValueError("audio file_path doesn't exist")
    # todo: check if it is .wav file
    [sampleRate, audio] = wavfile.read(file_path)
    #print("sampleRate, len(audio)", sampleRate, len(audio))
    
    filePrefix = os.path.basename(file_path).split('/')[-1].split('.')[0]
    
    if os.path.isdir(savePath) != True:
        os.makedirs(savePath)
        
    for i, json in enumerate(jsonArr):
        
        #print(i, json)
        begin = int(int(json['bg']) * sampleRate / 1000)
        end = int(int(json['ed']) * sampleRate / 1000)
        time_span = (int(json['ed']) - int(json['bg'])) /1000
        audioSeg = audio[begin:end]
        
        if time_span < low_th:
            """remove sentence audio if it is too short e.g., < 3 s"""
            continue
        elif time_span <= high_th:
            """save audio file to the savePath if it is between 3s and 6s
               File format : savePath/originalFileName_speaker_begin_end.wav
               E.g., audio = wavfile.read(originalFileName)
                     sent_audio = audio[begin:end]
            """
            newFilePath = "{}/{}__sp{}__beg{}_end{}.wav".format(savePath, filePrefix, json['speaker'], str(begin),str(end))
            wavfile.write(newFilePath, sampleRate, np.array(audioSeg, dtype="int16"))
        else:
            """For sentence audio that is longer than 6s, we divide it equally into '3s' sub-segments
               File format : savePath/originalFileName_speaker_begin_end.wav
               E.g., audio = wavfile.read(originalFileName)
                     sent_audio = audio[begin:end]
            """
            #print(int(time_span))
        
            segs = int(int(time_span) / low_th)
               
            #index = [int(time_span) % i for i in range(low_th,high_th+1)].index(0)
            #print(index)
            #time_span_seg = range(low_th,high_th+1)[index]
            
            slice_array = shape_split(audioSeg.shape, segs)               
            for i in range(segs):
                b = slice_array[i][0]
                #print(b.start, b.stop)
                audioSeg_seg = audio[begin+b.start:begin+b.stop]
                newFilePath = "{}/{}__sp{}__beg{}_end{}.wav".format(savePath, filePrefix,json['speaker'], 
                               str(begin+b.start),str(begin+b.stop))
                wavfile.write(newFilePath, sampleRate, np.array(audioSeg_seg, dtype="int16")) 
#            for j, audioSeg_seg in enumerate(np.array_split(audioSeg, segs)):
#                newFilePath = "{}/{}__sp{}__{}_{}.wav".format(savePath, filePrefix,json['speaker'], str(i),str(j))
#                wavfile.write(newFilePath, sampleRate, np.array(audioSeg_seg, dtype="int16")) 

for b_item in b:
    print(b_item)
    if b_item:
        dict(y.replace('"', '').split(':') for y in b_item.strip(',{').split(','))




input_path = '/Users/wangwei/Developer/Repository/wav'
output_path = '/Users/wangwei/Developer/Repository/wav_liudong_tag'
from os import listdir
from os.path import isfile, join
import pandas as pd
json_file = 'Clevo-Raw-Speech-Table1.csv'
df = pd.read_csv(json_file, usecols=[0,4], encoding='latin-1')
json_list = list(df['fileName (S)'].values)
#list1 = [os.path.basename(f).split('.')[0] for f in listdir(input_path) if isfile(join(input_path, f))]
def read_patch(input_dir, output_dir):
    
    onlyfiles = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    
    for file_name in onlyfiles:
        
        filePrefix = os.path.basename(file_name).split('.')[0]
        
        # create jsonArr
        if filePrefix in json_list:
            file_path = join(input_path,file_name)
            #print(file_name)
            jsonArr_str = df[df['fileName (S)'] == filePrefix]['transcriptionText (S)'].values[0]
            b = [x for x in jsonArr_str.strip("[]").split("}")]
            jsonArr = []
            for b_item in b:
                if not b_item:
                    continue
                print(file_name)
                try: 
                    jsonArr.append(dict(y.replace('"', '').split(':') for y in b_item.strip(',{').split(',')))
                except:
                    pass
        
        # run 
        segment_wav_may(jsonArr,file_path, output_path) #  write .wav files into output path 
        









