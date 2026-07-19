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

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=VGG19_service/requirements.txt,target=VGG19_service/requirements.txt \
    python -m pip install -r VGG19_service/requirements.txt

ARG KAGGLE_USERNAME
ARG KAGGLE_KEY

RUN mkdir -p /root/.config/kaggle && \
    echo "{\"username\":\"$KAGGLE_USERNAME\",\"key\":\"$KAGGLE_KEY\"}" > /root/.config/kaggle/kaggle.json && \
    chmod 600 /root/.config/kaggle/kaggle.json

RUN kaggle kernels output aziz0220/real-deep-learning-project/VGG19.keras -p .

COPY ./dataset/metal.wav .

EXPOSE 8000

CMD python app.py
