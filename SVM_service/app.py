from flask import Flask, request, jsonify
import librosa
import numpy as np
import joblib  # Assuming you're saving and loading your model with joblib
import base64


app = Flask(__name__)

# Load the pre-trained SVC model
classifier = joblib.load('svm_model.pkl')  # Make sure to replace with your actual model path

def extract_features(file_path):
    # Load the audio file
    x, sr = librosa.load(file_path)
    
    # Extract the zero-crossing rate and spectral centroid
    zero_cross_rate = sum(librosa.zero_crossings(x, pad=False))
    spectral_centroid = round(np.mean(librosa.feature.spectral_centroid(y=x, sr=sr)), 2)
    
    return np.array([[zero_cross_rate, spectral_centroid]])  # Return as a 2D array

@app.route('/classify_genre', methods=['POST'])
def classify_genre():
    data = request.json
    wav_music = data['wav_music']
    
    # Decode the base64 WAV file
    wav_bytes = base64.b64decode(wav_music)
    
    # Save the WAV file temporarily for processing
    with open('temp.wav', 'wb') as temp_wav:
        temp_wav.write(wav_bytes)

    # Extract features from the temporary WAV file
    features = extract_features('temp.wav')

    # Make prediction
    prediction = classifier.predict(features)
    
    return jsonify({'genre': prediction[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)