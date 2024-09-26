from flask import Flask, request, jsonify
import numpy as np
import librosa
import pickle
import base64
import os

app = Flask(__name__)

# Load the trained SVM model from the pickle file
with open('svm_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Function to decode base64 to a WAV file
def decode_base64_wav(base64_string, output_file='temp.wav'):
    with open(output_file, 'wb') as wav_file:
        wav_file.write(base64.b64decode(base64_string))

# Function to extract features from the WAV file (e.g., MFCC, Chroma)
def extract_features(wav_file):
    y, sr = librosa.load(wav_file, sr=None)
    
    # Example features (you can add more features)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    
    # Combine all features into a single array
    features = np.hstack([np.mean(mfccs.T, axis=0),
                          np.mean(chroma.T, axis=0),
                          np.mean(spectral_contrast.T, axis=0)])
    
    return features

@app.route('/classify_genre', methods=['POST'])
def classify_genre():
    try:
        # Retrieve the base64-encoded WAV music from the request
        data = request.json
        base64_wav = data.get('wav_music')

        if not base64_wav:
            return jsonify({'error': 'No wav_music provided'}), 400
        
        # Decode the base64 WAV file
        decode_base64_wav(base64_wav, 'temp.wav')
        
        # Extract features from the WAV file
        features = extract_features('temp.wav')
        
        # Ensure the feature vector is 2D as the model expects
        features = features.reshape(1, -1)
        
        # Make a prediction with the loaded model
        predicted_genre = model.predict(features)[0]
        
        # Cleanup temp file
        os.remove('temp.wav')
        
        # Return the predicted genre as a response
        return jsonify({'predicted_genre': predicted_genre})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
