# Simple Todo API

A lightweight RESTful Todo API built with **Python, Flask, Pytest, Jenkins, Docker, and GitHub**, demonstrating an automated CI/CD workflow from source control to deployment.

## Overview

This project demonstrates an end-to-end CI/CD pipeline:

```text
GitHub Push
     ↓
GitHub Webhook
     ↓
Jenkins
     ↓
Checkout
     ↓
Lint (Flake8)
     ↓
Unit Test (Pytest)
     ↓
Docker Build
     ↓
Deploy Container
     ↓
Smoke Test (/health)
```

If linting or tests fail, the pipeline stops and the application is not deployed.

## Tech Stack

| Category         | Technology     |
| ---------------- | -------------- |
| Backend          | Python / Flask |
| Testing          | Pytest         |
| Code Quality     | Flake8         |
| CI/CD            | Jenkins        |
| Containerization | Docker         |
| Source Control   | Git / GitHub   |
| Integration      | GitHub Webhook |

## Project Structure

```text
simple-todo-api/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
└── .gitignore
```

## API

| Method | Endpoint      | Description   |
| ------ | ------------- | ------------- |
| GET    | `/health`     | Health check  |
| GET    | `/todos`      | Get all todos |
| GET    | `/todos/<id>` | Get a todo    |
| POST   | `/todos`      | Create a todo |
| PUT    | `/todos/<id>` | Update a todo |
| DELETE | `/todos/<id>` | Delete a todo |

## Local Development

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

Run tests:

```bash
pytest tests/ -v
```

Start the application:

```bash
python app/main.py
```

The API will be available at:

```text
http://localhost:5000
```

## Docker

Build the image:

```bash
docker build -t simple-todo-api .
```

Run the container:

```bash
docker run -d \
  --name simple-todo-api \
  -p 5000:5000 \
  simple-todo-api
```

Or use Docker Compose:

```bash
docker compose up --build
```

## CI/CD Pipeline

The Jenkins pipeline is defined as code in `Jenkinsfile`.

### Pipeline Stages

```text
Checkout
   ↓
Install Dependencies
   ↓
Lint
   ↓
Unit Test
   ↓
Docker Build
   ↓
Deploy
   ↓
Smoke Test
```

### Deployment

After all validation steps pass, Jenkins builds a versioned Docker image:

```text
simple-todo-api:${BUILD_NUMBER}
```

The previous container is replaced with the new version.

### Smoke Test

After deployment, Jenkins verifies the service:

```bash
curl --fail http://localhost:5001/health
```

Expected response:

```json
{
  "status": "ok"
}
```

This ensures the newly deployed container is running and responding correctly.

## Key Engineering Practices

* **CI automation** — automatically run linting and tests on every push.
* **Pipeline as Code** — Jenkins pipeline is version-controlled through `Jenkinsfile`.
* **Containerized deployment** — package the application as a Docker image.
* **Build versioning** — use Jenkins Build Number to identify Docker images.
* **Deployment verification** — perform a post-deployment health check.
* **Failure protection** — failed validation prevents deployment.

## Future Improvements

* Add `pytest-cov` and coverage thresholds
* Push images to Docker Registry
* Add staging / production environments
* Add Discord / Slack notifications
* Introduce database persistence
* Deploy to Kubernetes

## CI/CD Result

The complete workflow is:

```text
Developer
   ↓
Git Push
   ↓
GitHub
   ↓ Webhook
Jenkins
   ↓
Test & Validate
   ↓
Docker Build
   ↓
Deploy
   ↓
Smoke Test
   ↓
SUCCESS
```
