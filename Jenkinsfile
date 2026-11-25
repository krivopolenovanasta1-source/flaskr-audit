pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Получение исходного кода'
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                echo 'Установка зависимостей'

                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/pip install -e .
                    .venv/bin/pip install pytest pytest-cov
                '''
            }
        }

        stage('Tests') {
            steps {
                echo 'Автоматизированное тестирование'

                sh '''
                    .venv/bin/pytest -v \
                    --cov=flaskr \
                    --cov-report=term \
                    --cov-report=xml:coverage.xml \
                    --junitxml=pytest-report.xml
                '''
            }

            post {
                always {
                    junit 'pytest-report.xml'
                }
            }
        }

        stage('SAST Analysis') {
            steps {
                echo 'Статический анализ исходного кода'

                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Все этапы Pipeline успешно выполнены'
        }

        failure {
            echo 'Обнаружена ошибка выполнения Pipeline'
        }

        always {
            archiveArtifacts(
                artifacts: 'coverage.xml,pytest-report.xml',
                allowEmptyArchive: true
            )
        }
    }
}
