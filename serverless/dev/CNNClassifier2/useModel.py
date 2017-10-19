from keras.models import load_model
import numpy as np
from random import randint

model = load_model('emotion_model.h5')
model.load_weights('emotion_model_weights.h5')

# Load data
x_all = np.load("IEMOCAP_X.npy")
y_all = np.load("IEMOCAP_Y.npy")

index = randint(0, x_all.shape[0])
data = x_all[index]
inputData = data.reshape(1, data.shape[0], data.shape[1], 1)

result = model.predict(inputData)

print(result)
print("actual result: {}".format(y_all[index]))

