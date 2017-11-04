from keras.models import load_model
from api import getMelspectrogram
import urllib.request

model = load_model('emotion_model.h5')
model.load_weights('emotion_model_weights.h5')

url = "https://s3-us-west-2.amazonaws.com/clevo.data/temp/Ses01M_impro04_F006.wav"
filename = "tmp.wav"

urllib.request.urlretrieve(url, filename)
# testfile = urllib.request.urlretrieve
# testfile.retrieve(url, path)

wavPath = filename

result = getMelspectrogram(wavPath)

if len(result) == 0:
    print("wavPath too long")

else:
    # index = randint(0, x_all.shape[0])
    # data = x_all[index]
    inputData = result.reshape(1, result.shape[0], result.shape[1], 1)

    result = model.predict(inputData)

    print(result)
    # print("actual result: {}".format(y_all[index]))

