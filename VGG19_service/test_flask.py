import os
import pytest
from app import app

@pytest.fixture
def client():
    # Configure Flask app for testing
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_vgg19_service_no_file(client):
    # Test endpoint without a file
    response = client.post('/vgg19_service')
    assert response.status_code == 400
   # assert b"No file part" in response.data
   # assert response.json['description'] == "No file part in the request"



