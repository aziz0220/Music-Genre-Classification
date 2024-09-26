import librosa
import numpy as np

def extract_features(wav_file):
    try:
        # Charger l'audio
        y, sr = librosa.load(wav_file, sr=None)

        # Calculer les caractéristiques: MFCC (Mel-frequency cepstral coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfccs_mean = np.mean(mfccs.T, axis=0)

        # Retourner les caractéristiques extraites
        return mfccs_mean
    except Exception as e:
        raise ValueError(f"Erreur lors de l'extraction des caractéristiques: {str(e)}")
