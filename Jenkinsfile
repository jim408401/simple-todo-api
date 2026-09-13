// Jenkinsfile - 使用「宣告式 Pipeline」語法（Pipeline as Code）
// 面試時可以強調：pipeline 定義跟著程式碼一起進版控，而不是在 Jenkins UI 上手動點設定

pipeline {
    agent any

    environment {
        // Docker image 的名稱與 tag，用 build number 讓每次 build 都有獨立版本
        IMAGE_NAME = "simple-todo-api"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        // 如果要推到 Docker Hub，帳密建議用 Jenkins Credentials 管理，不要寫死在這裡
        // DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id')
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code from Git...'
                checkout scm
            }
        }

        stage('Set up Python environment') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                echo 'Running flake8 for code quality check...'
                sh '''
                    . venv/bin/activate
                    flake8 app/ tests/ --max-line-length=100 --exit-zero
                '''
                // --exit-zero: lint 失敗先不擋 pipeline，等你熟悉後可以拿掉讓它真的擋下不合格的 code
            }
        }

        stage('Unit Test') {
            steps {
                echo 'Running pytest...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ --junitxml=test-results.xml --cov=app --cov-report=xml
                '''
            }
            post {
                always {
                    // 讓 Jenkins 在 UI 上顯示測試報告與趨勢圖
                    junit 'test-results.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}..."
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
            }
        }

        // 選用：推送到 Docker Hub 或私有 registry
        // stage('Push Docker Image') {
        //     steps {
        //         withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials-id',
        //                                            usernameVariable: 'DOCKER_USER',
        //                                            passwordVariable: 'DOCKER_PASS')]) {
        //             sh '''
        //                 echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
        //                 docker tag ${IMAGE_NAME}:${IMAGE_TAG} $DOCKER_USER/${IMAGE_NAME}:${IMAGE_TAG}
        //                 docker push $DOCKER_USER/${IMAGE_NAME}:${IMAGE_TAG}
        //             '''
        //         }
        //     }
        // }

        stage('Deploy') {
            steps {
                echo 'Deploying new container...'
                sh '''
                    docker stop todo-api-container || true
                    docker rm todo-api-container || true
                    docker run -d --name todo-api-container -p 5000:5000 ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                echo 'Verifying deployment with a health check...'
                sh '''
                    sleep 5
                    curl --fail http://localhost:5000/health
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! ✅'
        }
        failure {
            echo 'Pipeline failed. Check the logs above. ❌'
        }
        always {
            // 清理舊的 image，避免佔用磁碟空間
            sh 'docker image prune -f || true'
        }
    }
}
