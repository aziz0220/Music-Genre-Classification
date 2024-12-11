import os
import pytest
from io import BytesIO
from app import app  # Import the Flask app from your app.py

# Test configuration
@pytest.fixture
def client():
    """Fixture for setting up the test client."""
    with app.test_client() as client:
        yield client

def test_classify_genre_no_file(client):
    """Test if the '/classify_genre' route returns a 400 error when no file is provided."""
    response = client.post('/classify_genre')
    assert response.status_code == 400
    assert b"No file part" in response.data

def test_classify_genre_empty_file(client):
    """Test if the '/classify_genre' route returns a 400 error when an empty file is provided."""
    data = {
        'wav_file': (BytesIO(b''), 'empty.wav')
    }
    response = client.post('/classify_genre', data=data)
    assert response.status_code == 400
    assert b"No selected file" in response.data

def test_classify_genre_valid_file(client):
    """Test if the '/classify_genre' route returns a valid genre prediction."""
    with open("metal.wav", "rb") as f:
        data = {
            'wav_file': (f, 'metal.wav')
        }
        response = client.post('/classify_genre', data=data)
        assert response.status_code == 200
        assert response.json['genre'] == 'metal'

