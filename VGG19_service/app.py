from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
import librosa
import librosa.display
import tensorflow as tf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random
import warnings
import requests
import zipfile
import io

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

def setRandom():
    seed = 0
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    tf.compat.v1.set_random_seed(seed)

def download_model():
    model_path = 'VGG19.keras'
    if os.path.exists(model_path):
        return True
    print("Downloading VGG19 model at runtime...")
    url = "https://www.kaggle.com/api/v1/kernels/output/aziz0220/real-deep-learning-project"
    token = os.environ.get('KAGGLE_API_TOKEN', '')
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    try:
        resp = requests.get(url, headers=headers, timeout=300, allow_redirects=True)
        if resp.status_code != 200:
            print(f"Kaggle API error: {resp.status_code}")
            return False
        z = zipfile.ZipFile(io.BytesIO(resp.content))
        keras_files = [f for f in z.namelist() if '.keras' in f or '.h5' in f]
        if not keras_files:
            print("No model files in archive")
            return False
        with z.open(keras_files[0]) as f:
            with open(model_path, 'wb') as out:
                out.write(f.read())
        print("Model downloaded at runtime.")
        return True
    except Exception as e:
        print(f"Runtime download failed: {e}")
        return False

print("Initializing VGG19 service...")
if not os.path.exists('VGG19.keras'):
    download_model()
try:
    model = load_model('VGG19.keras')
    model.trainable = False
    print("Model loaded.")
except Exception as e:
    print(f"Model load failed: {e}")
    model = None

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

@app.route('/vgg19_service', methods=['POST'])
def vgg19_service():
    if model is None:
        return jsonify({'genre': 'error', 'description': 'Model not loaded'}), 503

    if 'wav_file' not in request.files:
        abort(400, description="No file part in the request")
    wav_file = request.files['wav_file']
    if wav_file.filename == '':
        abort(400, description="No selected file")
    temp_file_path = './temp_audio.wav'
    wav_file.save(temp_file_path)

    try:
        setRandom()
        file_data, samplingRate = librosa.load(temp_file_path)
        example, _ = librosa.effects.trim(file_data)
        hopLength = 512

        spectrogram = librosa.power_to_db(
            librosa.feature.melspectrogram(y=example, sr=samplingRate, n_fft=2048,
                                           hop_length=hopLength, n_mels=128, power=4.0),
            ref=np.max
        )
        imgSize = (288, 432)
        dpi = 72
        figsize = (imgSize[1] / dpi, imgSize[0] / dpi)
        plt.figure(figsize=figsize, dpi=dpi)
        librosa.display.specshow(spectrogram)
        temp_img_path = 'temp_spectrogram.png'
        plt.savefig(temp_img_path)
        plt.close()

        image = tf.cast(
            tf.image.resize(
                tf.image.decode_png(tf.io.read_file(temp_img_path), channels=3),
                imgSize
            ),
            tf.float32
        ) / 255.0

        mel_spectrogram = tf.image.convert_image_dtype(image, tf.float32)
        mel_spectrogram = np.expand_dims(mel_spectrogram, axis=0)
        prediction = model.predict(mel_spectrogram)

        genreMap = {
            "blues": 0, "classical": 1, "country": 2, "disco": 3,
            "hiphop": 4, "jazz": 5, "metal": 6, "pop": 7, "reggae": 8, "rock": 9
        }
        inverseGenreMap = {value: key for key, value in genreMap.items()}
        predicted_genre = inverseGenreMap[np.argmax(prediction)]

        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
        os.remove(temp_file_path)

        return jsonify({'genre': predicted_genre})

    except Exception as e:
        for p in [temp_file_path, 'temp_spectrogram.png']:
            if os.path.exists(p):
                os.remove(p)
        return jsonify({'genre': 'error', 'description': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
