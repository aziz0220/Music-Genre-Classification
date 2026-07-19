FROM python:3.10.5-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY VGG19_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG KAGGLE_API_TOKEN
ENV KAGGLE_API_TOKEN=${KAGGLE_API_TOKEN:-}

RUN mkdir -p /root/.config/kaggle

RUN kaggle kernels output aziz0220/real-deep-learning-project/VGG19.keras -p .

COPY VGG19_service/app.py .
COPY dataset/metal.wav .

EXPOSE 8000

CMD python app.py
