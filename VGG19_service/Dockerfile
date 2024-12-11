FROM python:3.10.5-slim-buster

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
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

# Ensure the .kaggle directory exists and copy kaggle.json
RUN mkdir -p ../root/.kaggle && echo "$KAGGLE_JSON" > ../root/.kaggle/kaggle.json


# COPY /VGG19_service/kaggle.json ../root/.config/kaggle/kaggle.json

#RUN kaggle kernels output aziz0220/real-deep-learning-project -p .


EXPOSE 8000

CMD python app.py
