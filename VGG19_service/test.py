import requests
from tensorflow.keras.models import load_model
import numpy as np
import librosa
import librosa.display
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt
import os

def wav_to_image(filePath):
    file, samplingRate = librosa.load(filePath)
    example, _ = librosa.effects.trim(file)
    hopLength = 512
    spectrogram = librosa.power_to_db(librosa.feature.melspectrogram(y = example, sr = samplingRate, n_fft = 2048, hop_length = hopLength, n_mels = 128, power = 4.0 ), ref = np.max)
    imgSize = (288, 432)
    plt.figure(figsize=(imgSize[1] / 100, imgSize[0] / 100), dpi=100)
    plt.axis('off')
    librosa.display.specshow(spectrogram, sr = samplingRate, hop_length = hopLength, x_axis = "off", y_axis = "off")
    temp_img_path = 'temp_spectrogram.png'
    plt.savefig(temp_img_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    image = tf.image.decode_png(tf.io.read_file(temp_img_path), channels=3)
    image = tf.image.resize(image, imgSize)
    # Normalize the pixel values between 0 and 1
    image = tf.cast(image, tf.float32) / 255.0
    image = np.expand_dims(image, axis = 0)
    return image

genreMap = {
    "blues": 0,
    "classical": 1,
    "country": 2,
    "disco": 3,
    "hiphop": 4,
    "jazz": 5,
    "metal": 6,
    "pop": 7,
    "reggae": 8,
    "rock": 9
}
inverseGenreMap = {value: key for key, value in genreMap.items()}
model=load_model('model.keras')

file_path = 'metal.wav'
spectrogram_image = wav_to_image(file_path)
predictions = model.predict(spectrogram_image)
predictedGenre = inverseGenreMap[np.argmax(predictions)]
print(f"\033[1mPredicted genre:\033[0m {predictedGenre}")
print(f"\033[1mActual genre:\033[0m {file_path}")


def test_vgg_service():
    url = "http://localhost:5001/classify_genre"
    data = {'wav_music': ''}
    response = requests.post(url, data=data)
    
    assert response.status_code == 200
    assert 'genre' in response.json()

