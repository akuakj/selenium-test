pipeline {
    agent any

    triggers {
        cron('0 9 * * *')
    }

    environment {
        EMAIL_RECIPIENT = 'your@email.com'
    }

    stages {
        stage('Install dependencies') {
            steps {
                bat 'pip install pytest allure-pytest faker playwright pytest-xdist'
                bat 'pip install -r requirements.txt'
                bat 'playwright install chromium'
            }
        }

        stage('Run tests') {
            steps {
                bat '''
                    pytest tests/ ^
                        --alluredir=allure-results ^
                        -v ^
                        --tb=short ^
                        --maxfail=5 ^
                        --strict-markers
                '''
            }
        }

        stage('Generate Allure report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            echo "Build finished with status: ${currentBuild.result}"
        }
        success {
            echo '✅ All tests passed!'
        }
        failure {
            echo '❌ Some tests failed!'
        }
    }
}