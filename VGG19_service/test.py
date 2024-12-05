import requests

def test_vgg_service():
    url = "http://localhost:5001/classify_genre"
    data = {'wav_music': ''}
    response = requests.post(url, data=data)
    
    assert response.status_code == 200
    assert 'genre' in response.json()

