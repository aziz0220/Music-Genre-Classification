from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import librosa
import librosa.display
import tensorflow as tf
from PIL import Image

import os

app = Flask(__name__)

# Load your pre-trained model (VGG19)
model = load_model('model.keras')


def wav_to_image(filePath):
    # Load audio file
    file, samplingRate = librosa.load(filePath)
    print(file.shape, samplingRate)

    # Trim silence from the beginning and end
    example, _ = librosa.effects.trim(file)
    hopLength = 512

    # Generate mel spectrogram
    spectrogram = librosa.power_to_db(
        librosa.feature.melspectrogram(y=example, sr=samplingRate, n_fft=2048, hop_length=hopLength, n_mels=128,
                                       power=4.0),
        ref=np.max
    )

    # Resize spectrogram to fit your desired image size
    imgSize = (288, 432)

    # Use PIL to save the image directly
    pil_img = Image.fromarray(spectrogram, mode='L')  # 'L' mode for grayscale
    pil_img = pil_img.resize(imgSize)  # Resize to target size
    temp_img_path = 'temp_spectrogram.png'
    pil_img.save(temp_img_path)
    # Read the saved image using TensorFlow
    image = tf.image.decode_png(tf.io.read_file(temp_img_path), channels=3)
    image = tf.image.resize(image, imgSize)
    image = image / 255.0  # Normalize pixel values between 0 and 1
    # Clean up the temporary image
    os.remove(temp_img_path)
    return image


# Function to predict genre
def predict_genre(wav_file):
    mel_spectrogram = wav_to_image(wav_file)
    mel_spectrogram = np.expand_dims(mel_spectrogram, axis=0)  # Expand dimensions for batch
    prediction = model.predict(mel_spectrogram)
    genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    predicted_genre = genres[np.argmax(prediction)]
    return predicted_genre


@app.route('/vgg19_service', methods=['POST'])
def vgg19_service():
    if 'wav_file' not in request.files:
        abort(400, description="No file part in the request")
    wav_file = request.files['wav_file']
    if wav_file.filename == '':
        abort(400, description="No selected file")
    temp_file_path = './temp_audio.wav'
    wav_file.save(temp_file_path)

    # Predict genre
    predicted_genre = predict_genre(temp_file_path)

    # Clean up temporary audio file
    os.remove("temp_audio.wav")

    return jsonify({'predicted_genre': predicted_genre})


@app.route('/')
def upload_form():
    return '''
        <!doctype html>
        <html>
        <head><title>Upload WAV file With VGG 19</title></head>
        <body>
            <h2>Upload a WAV file to classify its genre with VGG19</h2>
            <form action="/vgg19_service" method="post" enctype="multipart/form-data">
                <input type="file" name="wav_file" accept=".wav" required>
                <button type="submit">Upload and Classify</button>
            </form>
        </body>
        </html>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)