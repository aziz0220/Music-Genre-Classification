from flask import Flask, request, jsonify, abort, render_template
import librosa
import numpy as np
import joblib

import os

app = Flask(__name__)


classifier = joblib.load('model.pkl')
scaler = joblib.load('scl.pkl')


def extract_features(filename):
    y, sr = librosa.load(filename, duration=30)

    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_stft_mean = np.mean(chroma_stft)
    chroma_stft_var = np.var(chroma_stft)

    rms = librosa.feature.rms(y=y)
    rms_mean = np.mean(rms)
    rms_var = np.var(rms)

    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_centroid_mean = np.mean(spectral_centroid)
    spectral_centroid_var = np.var(spectral_centroid)

    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_bandwidth_mean = np.mean(spectral_bandwidth)
    spectral_bandwidth_var = np.var(spectral_bandwidth)

    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85)
    rolloff_mean = np.mean(rolloff)
    rolloff_var = np.var(rolloff)

    zero_crossing_rate = librosa.feature.zero_crossing_rate(y=y)
    zero_crossing_rate_mean = np.mean(zero_crossing_rate)
    zero_crossing_rate_var = np.var(zero_crossing_rate)

    harmonic, percussive = librosa.effects.hpss(y)
    harmony_mean = np.mean(harmonic)
    harmony_var = np.var(harmonic)

    perceptual_mean = np.mean(harmonic)
    perceptual_var = np.var(harmonic)

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_means = np.mean(mfcc, axis=1)
    mfcc_vars = np.var(mfcc, axis=1)

    features = [
        chroma_stft_mean,
        chroma_stft_var,
        rms_mean,
        rms_var,
        spectral_centroid_mean,
        spectral_centroid_var,
        spectral_bandwidth_mean,
        spectral_bandwidth_var,
        rolloff_mean,
        rolloff_var,
        zero_crossing_rate_mean,
        zero_crossing_rate_var,
        harmony_mean,
        harmony_var,
        perceptual_mean,
        perceptual_var,
        tempo[0]
    ]

    for i in range(0, 20):
        features.append(mfcc_means[i])
        features.append(mfcc_vars[i])

    return np.array(features).reshape(1, -1)


@app.route('/')
def upload_form():
    return '''
        <!doctype html>
        <html>
        <head><title>Upload WAV file</title></head>
        <body>
            <h2>Upload a WAV file to classify its genre With SVM</h2>
            <form action="/classify_genre" method="post" enctype="multipart/form-data">
                <input type="file" name="wav_file" accept=".wav" required>
                <button type="submit">Upload and Classify</button>
            </form>
        </body>
        </html>
    '''


@app.route('/classify_genre', methods=['POST'])
def classify_genre():

    if 'wav_file' not in request.files:
        abort(400, description="No file part in the request")

    wav_file = request.files['wav_file']
    if wav_file.filename == '':
        abort(400, description="No selected file")

    temp_file_path = 'temp.wav'
    wav_file.save(temp_file_path)

    features = extract_features(temp_file_path).round(3)

    features_scaled = scaler.transform(features).round(3)

    prediction = classifier.predict(features_scaled)

    os.remove(temp_file_path)

    return jsonify({'genre': prediction[0]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
