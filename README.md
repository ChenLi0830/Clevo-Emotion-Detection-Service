# Clevo-Emotion-Detection-Service
Performing emotion recognition from audio files. The Time sequence audio data is transformed into frequency data by performing Fourier transform. The frequency data is treated as images to avoid different time durations. Then the emotion recogniton is performed by using Convolutional Neural Network (CNN) Categorization. 

## Development
Emotion recognition Service
```
cd ./server/dockerVersion
docker-compose up -d
```

Emotion audio file preprocessing
```
cd serverless
npm install
```

