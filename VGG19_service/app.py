import base64
import io
import librosa
import numpy as np
import pickle
from flask import Flask, request, jsonify
from utils import extract_features

# Charger le modèle SVM pré-entraîné
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    if 'wav_music' not in data:
        return jsonify({"error": "wav_music key is missing"}), 400

    # Décoder le fichier wav en base64
    wav_music_base64 = data['wav_music']
    try:
        wav_data = base64.b64decode(wav_music_base64)
        wav_file = io.BytesIO(wav_data)

        # Extraire les caractéristiques audio
        features = extract_features(wav_file)

        # Prédiction du genre
        prediction = model.predict([features])
        return jsonify({"genre": prediction[0]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
