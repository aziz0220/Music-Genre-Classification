# Assuming you have trained the VGG19 model already
from tensorflow.keras.applications import VGG19
from tensorflow.keras.models import load_model
import numpy as np
import librosa
import tensorflow as tf
from flask import Flask, request, jsonify
import base64
import io
from pydub import AudioSegment

app = Flask(__name__)

# Load your pre-trained model (VGG19)
model = load_model('vgg19_model.h5')  # Path to your saved model

# Function to process wav file and convert to mel spectrogram
def wav_to_mel_spectrogram(wav_file):
    y, sr = librosa.load(wav_file)
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
    spectrogram = tf.image.resize(spectrogram, (224, 224))  # Resize for VGG19 input
    spectrogram = np.stack([spectrogram, spectrogram, spectrogram], axis=-1)  # Convert to 3 channels
    spectrogram = np.expand_dims(spectrogram, axis=0)  # Add batch dimension
    return spectrogram

# Function to predict genre
def predict_genre(wav_file):
    mel_spectrogram = wav_to_mel_spectrogram(wav_file)
    prediction = model.predict(mel_spectrogram)
    genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    predicted_genre = genres[np.argmax(prediction)]
    return predicted_genre

@app.route('/vgg19_service', methods=['POST'])
def vgg19_service():
    data = request.json
    if 'wav_music' not in data:
        return jsonify({'error': 'No audio file provided'}), 400

    # Decode the base64 audio file
    wav_music_base64 = data['wav_music']
    wav_music = base64.b64decode(wav_music_base64)

    # Save the wav file
    wav_file = io.BytesIO(wav_music)
    audio = AudioSegment.from_file(wav_file, format='wav')
    audio.export("temp_audio.wav", format="wav")  # Save the file temporarily

    # Predict genre
    predicted_genre = predict_genre("temp_audio.wav")

    return jsonify({'predicted_genre': predicted_genre})

if __name__ == '__main__':
    app.run(debug=True)

