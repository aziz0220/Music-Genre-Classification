import requests, zipfile, io, os

url = "https://www.kaggle.com/api/v1/kernels/output/aziz0220/real-deep-learning-project"
token = os.environ.get('KAGGLE_API_TOKEN', '')
headers = {}
if token:
    headers['Authorization'] = f'Bearer {token}'

print("Downloading VGG19 model from Kaggle...")
resp = requests.get(url, headers=headers, timeout=300, allow_redirects=True)
print(f"Status: {resp.status_code}")

if resp.status_code != 200:
    print(f"API error: HTTP {resp.status_code}")
    print(f"Response: {resp.text[:500]}")
    exit(1)

z = zipfile.ZipFile(io.BytesIO(resp.content))
files = z.namelist()
print(f"Archive contains: {files}")

if 'VGG19.keras' in files:
    with z.open('VGG19.keras') as f:
        with open('VGG19.keras', 'wb') as out:
            out.write(f.read())
    print("Model extracted successfully.")
else:
    print(f"VGG19.keras not found in archive. Files: {files}")
    exit(1)
