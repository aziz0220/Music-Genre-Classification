from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return '<h1>VGG19 Music Genre Classifier</h1><p>Service is running.</p>'

@app.route('/vgg19_service', methods=['POST'])
def vgg19_service():
    return jsonify({'genre': 'unknown', 'status': 'model_not_loaded'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
