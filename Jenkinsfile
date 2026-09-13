pipeline {

    agent any

    environment {
        IMAGE_NAME = "simple-todo-api"
        CONTAINER_NAME = "simple-todo-api"
        PORT = "5000"
    }

    stages {

        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Install Dependencies") {
            steps {
                sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements-dev.txt
                """
            }
        }

        stage("Lint") {
            steps {
                sh """
                    . venv/bin/activate
                    flake8 app tests
                """
            }
        }

        stage("Unit Test") {
            steps {
                sh """
                    . venv/bin/activate
                    pytest tests/ -v
                """
            }
        }

        stage("Docker Build") {
            steps {
                sh """
                    docker build \
                        -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                        -t ${IMAGE_NAME}:latest \
                        .
                """
            }
        }

        stage("Deploy") {
            steps {
                sh """
                    docker rm -f ${CONTAINER_NAME} || true

                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${PORT}:5000 \
                        ${IMAGE_NAME}:${BUILD_NUMBER}
                """
            }
        }

        stage("Smoke Test") {
            steps {
                sh """
                    sleep 3

                    curl --fail \
                        http://localhost:${PORT}/health
                """
            }
        }
    }

    post {

        success {
            echo "CI/CD Pipeline completed successfully."
        }

        failure {
            echo "CI/CD Pipeline failed."
        }

        always {
            sh """
                docker ps -a
            """
        }
    }
}