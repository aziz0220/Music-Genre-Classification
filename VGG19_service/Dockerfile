FROM tensorflow/tensorflow:2.15.0

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY VGG19_service/requirements.txt .
RUN pip install --no-cache-dir --timeout 180 -r requirements.txt

COPY VGG19_service/app.py .
COPY dataset/metal.wav .

EXPOSE 8000

CMD python app.py
