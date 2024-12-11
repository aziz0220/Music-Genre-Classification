# Mini-Projet-Docker: Machine Learning Music Genre Classification

## Overview
This project is part of the **Mini Projet: Nouvelles Architectures** course at ENSIT. It demonstrates the use of Docker to integrate, deploy, and test a Machine Learning environment using Python and Flask. The goal is to classify music genres based on audio features extracted from the [GTZAN Dataset - Music Genre Classification](https://www.kaggle.com/andradaolteanu/gtzan-dataset-music-genre-classification).

---

## Features
1. **Music Genre Classification Services:**
    - **SVM Service:** A Flask-based web service that uses a Support Vector Machine (SVM) model to classify the genre of a WAV file.
    - **VGG19 Service:** A Flask-based web service that leverages the VGG19 neural network to classify the genre of a WAV file.
2. **Frontend Application:** A user-friendly interface to interact with the classification services.
3. **Dockerized Setup:** All components are containerized for seamless orchestration using Docker Compose.
4. **Continuous Integration and Testing:** Jenkins is configured for CI/CD to ensure smooth development and deployment workflows.

---

## Project Structure
```
Mini-Projet-Docker
├── .github/workflows    # GitHub Actions workflows for CI
├── SVM_service          # Flask service for SVM model
├── VGG19_service        # Flask service for VGG19 model
├── dataset              # Music dataset files
├── frontend             # Frontend application
├── models               # Pre-trained models
├── test                 # Test cases for services
├── docker-compose.yaml  # Docker Compose file to orchestrate services
└── Jenkinsfile          # Jenkins pipeline configuration
```

---

## Technologies Used
- **Machine Learning:**
  - SVM (Support Vector Machine)
  - VGG19 Neural Network
- **Web Framework:** Flask
- **Containerization:** Docker, Docker Compose
- **Continuous Integration/Deployment:** GitHub Actions, Jenkins
- **Frontend:** Next.JS

---

## Getting Started

### Prerequisites
- Install [Docker](https://www.docker.com/get-started)
- Install [Docker Compose](https://docs.docker.com/compose/install/)
- Optional: Install [Jenkins](https://www.jenkins.io/) for CI/CD or use the [Jenkins DOCKER instructions](https://www.jenkins.io/doc/book/installing/docker/)

### Setup and Run
1. **Clone the repository:**
   ```bash
   git clone https://github.com/aziz0220/Mini-Projet-Docker.git
   cd Mini-Projet-Docker
   ```
2. **Build and Run Containers:**
   ```bash
   docker compose up --build -d
   ```
3. **Access Services:**
   - **Frontend:** [http://localhost:3000](http://localhost:3000)
   - **SVM Service:** [http://localhost:5000](http://localhost:5000)
   - **VGG19 Service:** [http://localhost:5001](http://localhost:5001)

4. **Stop Containers:**
   ```bash
   docker compose down
   ```

---

## API Endpoints

### SVM Service
- **Endpoint:** `/classify`
- **Method:** POST
- **Input:** Base64-encoded WAV file
- **Output:** JSON with predicted genre

### VGG19 Service
- **Endpoint:** `/classify`
- **Method:** POST
- **Input:** Base64-encoded WAV file
- **Output:** JSON with predicted genre

---

## Continuous Integration (CI/CD)

### GitHub Actions
The repository includes workflows for:
- Building Docker images
- Running tests
- Deploying the application

### Jenkins
Jenkins is configured to automate the build, test, and deployment processes.

---

## Dataset
We use the [GTZAN Dataset](https://www.kaggle.com/andradaolteanu/gtzan-dataset-music-genre-classification) for training and testing models. Please ensure the dataset is downloaded and placed in the `dataset` directory before running the services.

---
## Kaggle Notebooks (for deploying MODELS)

- **VGG 19** [https://www.kaggle.com/code/aziz0220/real-deep-learning-project](VGG19.keras)

- ** SVM MODEL**[https://www.kaggle.com/code/aziz0220/svm-for-music-genres-classification](svm_model.pkl)

    


## Testing
- Tests are located in the `test` directory.
- Run tests using Docker:
  ```bash
  docker-compose run --rm test-runner
  ```

---

## Report
A detailed report of the project, including implementation details and results, is provided as a PDF.

---

## Authors
- **Aziz BEN AMOR**
- **Skander ABID**
---


