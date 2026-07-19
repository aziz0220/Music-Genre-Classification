FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY VGG19_service/requirements.txt .
RUN pip install --no-cache-dir --timeout 120 -r requirements.txt

COPY VGG19_service/app.py .
COPY dataset/metal.wav .

EXPOSE 8000

CMD python app.py
