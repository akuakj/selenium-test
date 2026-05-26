pipeline {
    agent any

    triggers {
        cron('0 9 * * *')
    }

    environment {
        EMAIL_RECIPIENT = 'your@email.com'
        PYTHONPATH = "${env.WORKSPACE}"
    }

    stages {
        stage('Install dependencies') {
            steps {
                bat 'C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python313\\python.exe --version'
                bat 'C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m pip install --upgrade pip'
                bat 'C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m pip install pytest allure-pytest faker playwright pytest-xdist'
                bat 'C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m pip install -r requirements.txt'
                bat 'C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m playwright install chromium'
            }
        }

        stage('Run tests') {
            steps {
                bat '''
                    set PYTHONPATH=%PYTHONPATH%;%CD%
                    C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m pytest tests/ ^
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