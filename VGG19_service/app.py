from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import numpy as np
import librosa
import librosa.display
import tensorflow as tf
from tensorflow.keras.models import Model, load_model, Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Conv2D, MaxPooling2D, Flatten, Dropout
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'VGG19.keras'

def setRandom():
    seed = 0
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

def ensure_model():
    if not os.path.exists(MODEL_PATH):
        print("Building CNN model from scratch...")
        m = Sequential([
            Conv2D(32, (3,3), activation='relu', input_shape=(288, 432, 3)),
            MaxPooling2D(2,2),
            Conv2D(64, (3,3), activation='relu'),
            MaxPooling2D(2,2),
            Conv2D(128, (3,3), activation='relu'),
            MaxPooling2D(2,2),
            Flatten(),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(10, activation='softmax')
        ])
        m.compile(optimizer='adam', loss='categorical_crossentropy')
        m.save(MODEL_PATH)
        print(f"Model saved to {MODEL_PATH}")
    return True

print("Initializing VGG19 service...")
try:
    ensure_model()
    model = load_model(MODEL_PATH)
    model.trainable = False
    print("Model loaded.")
except Exception as e:
    print(f"Model setup failed: {e}")
    import traceback
    traceback.print_exc()
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
