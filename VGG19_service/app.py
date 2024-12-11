from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
import librosa
import librosa.display
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt
import os
import random

def setRandom():
    seed = 0 # random seed value
    os.environ["PYTHONHASHSEED"] = str(seed) # if this is not set, a random value is used to seed the hashes of some objects
    random.seed(seed) # sets the base python and numpy random seeds
    np.random.seed(seed)
    tf.random.set_seed(seed) # sets the tensorflow random seed
    tf.compat.v1.set_random_seed(seed)

app = Flask(__name__)
CORS(app)

# Load your pre-trained model (VGG19)
model = load_model('model.keras')
model.trainable = False  # Set the model to inference mode (if needed)
print(model.summary())

def wav_to_image(filePath):
    # Load audio file
    file, samplingRate = librosa.load(filePath)
    #print(file.shape, samplingRate)

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
    dpi = 72
    figsize = (imgSize[1] / dpi, imgSize[0] / dpi)
    plt.figure(figsize=figsize, dpi=dpi)
   # plt.axis('off')
    librosa.display.specshow(spectrogram
                             #, sr=samplingRate, hop_length=hopLength
                             #, x_axis = "off", y_axis = "off"
                             )
    temp_img_path = 'temp_spectrogram.png'
    plt.savefig(temp_img_path, 
             #   bbox_inches='tight', pad_inches=0
                )
    plt.close()
    image = tf.cast(tf.image.resize(tf.image.decode_png(tf.io.read_file(temp_img_path), channels = 3), imgSize), tf.float32) / 255.0


    return image


# Function to predict genre
def predict_genre(wav_file):
    setRandom()
    mel_spectrogram = wav_to_image(wav_file)
    mel_spectrogram = tf.image.convert_image_dtype(mel_spectrogram, tf.float32)
    mel_spectrogram = np.expand_dims(mel_spectrogram, axis=0)
    print(model.input_shape)  # Expected shape (None, 224, 224, 3) for VGG
    print(mel_spectrogram.shape)  # Should be (1, 224, 224, 3)
    # Expand dimensions for batch
    prediction = model.predict(mel_spectrogram)
    print(prediction)
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
    #genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    #predicted_genre = genres[np.argmax(prediction)]
    predicted_genre = inverseGenreMap[np.argmax(prediction)]
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

    return jsonify({'genre': predicted_genre})


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
