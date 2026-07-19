import requests, zipfile, io, os, sys

url = "https://www.kaggle.com/api/v1/kernels/output/aziz0220/real-deep-learning-project"
token = os.environ.get('KAGGLE_API_TOKEN', '')

print(f"Python: {sys.version}")
print(f"Token present: {bool(token)}")
print(f"Token length: {len(token)}")

headers = {}
if token:
    headers['Authorization'] = f'Bearer {token}'

print(f"Downloading from: {url}")
try:
    resp = requests.get(url, headers=headers, timeout=300, allow_redirects=True)
    print(f"HTTP Status: {resp.status_code}")
    print(f"Content-Type: {resp.headers.get('Content-Type', 'N/A')}")
    print(f"Content-Length: {resp.headers.get('Content-Length', 'N/A')}")

    if resp.status_code != 200:
        print(f"Response body: {resp.text[:1000]}")
        print("Continuing without model (will download at runtime)")
        sys.exit(0)

    z = zipfile.ZipFile(io.BytesIO(resp.content))
    files = z.namelist()
    print(f"Archive contains ({len(files)} files): {files}")

    keras_files = [f for f in files if '.keras' in f or '.h5' in f]
    if keras_files:
        target = keras_files[0]
        with z.open(target) as f:
            with open('VGG19.keras', 'wb') as out:
                out.write(f.read())
        print(f"Model saved as VGG19.keras from {target}")
    else:
        print(f"No .keras or .h5 files found in archive")
        sys.exit(0)

except Exception as e:
    print(f"Download error: {e}")
    print("Continuing without model (will download at runtime)")
    sys.exit(0)
