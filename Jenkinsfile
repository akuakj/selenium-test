pipeline {
    agent any

    triggers {
        cron('0 8 * * *')
    }

    environment {
        PYTHON     = "C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
        ALLURE_RESULTS = "${WORKSPACE}\\allure-results"
        ALLURE_REPORT  = "${WORKSPACE}\\allure-report"

        DB_HOST = credentials('DB_HOST')
        DB_PORT = credentials('DB_PORT')
        DB_USER = credentials('DB_USER')
        DB_PASS = credentials('DB_PASS')
        DB_NAME = credentials('DB_NAME')

        REPORT_RECIPIENT = 'x00004e@gmail.com'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        timeout(time: 60, unit: 'MINUTES')
        timestamps()
    }

    stages {

        stage('Setup Environment') {
            steps {
                echo '=== Установка зависимостей ==='
                bat """
                    "${PYTHON}" -m pip install --upgrade pip --quiet
                    "${PYTHON}" -m pip install -r requirements.txt --quiet
                """

                echo '=== Установка браузеров Playwright ==='
                bat '"${PYTHON}" -m playwright install chromium'

                echo '=== Очистка предыдущих результатов ==='
                bat """
                    if exist allure-results rmdir /s /q allure-results
                    if exist allure-report rmdir /s /q allure-report
                    mkdir allure-results
                """
            }
        }

        stage('API Tests') {
            steps {
                echo '=== Запуск API-тестов ==='
                bat """
                    set PYTHONPATH=${WORKSPACE}
                    "${PYTHON}" -m pytest tests/tests_api/ ^
                        --alluredir=allure-results ^
                        --tb=short ^
                        -q ^
                        --continue-on-collection-errors
                    exit /b 0
                """
            }
        }

        stage('UI Tests (Selenium)') {
            steps {
                echo '=== Запуск UI-тестов (Selenium) ==='
                bat """
                    set PYTHONPATH=${WORKSPACE}
                    "${PYTHON}" -m pytest tests/test_ui/ ^
                        --alluredir=allure-results ^
                        --tb=short ^
                        -q ^
                        --continue-on-collection-errors
                    exit /b 0
                """
            }
        }


        stage('Generate Allure Report') {
            steps {
                echo '=== Генерация Allure HTML-отчёта ==='
                bat 'allure generate allure-results --output allure-report --clean'
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk              : '',
                    results          : [[path: 'allure-results']],
                    report           : 'allure-report'
                ])
            }
        }

        stage('Archive Report') {
            steps {
                bat 'powershell Compress-Archive -Path allure-report -DestinationPath allure-report.zip -Force'
                archiveArtifacts artifacts: 'allure-report.zip', fingerprint: true
            }
        }
    }

    post {
        always {
            script {
                def summary = ''
                def summaryFile = "${ALLURE_REPORT}\\widgets\\summary.json"
                if (fileExists(summaryFile)) {
                    def json    = readJSON file: summaryFile
                    def stat    = json.statistic
                    def passed  = stat.passed  ?: 0
                    def failed  = stat.failed  ?: 0
                    def broken  = stat.broken  ?: 0
                    def skipped = stat.skipped ?: 0
                    def total   = stat.total   ?: 0
                    summary = """
Результаты тестов:
  Passed : ${passed}
  Failed : ${failed}
  Broken : ${broken}
  Skipped: ${skipped}
  Total  : ${total}
"""
                } else {
                    summary = 'Файл summary.json не найден — отчёт мог не сгенерироваться.'
                }

                def buildStatus = currentBuild.currentResult ?: 'UNKNOWN'
                def subject = "[Jenkins] ЗАГС автотесты — ${buildStatus} | сборка #${BUILD_NUMBER}"
                def body = """
Привет!

Автоматический прогон тестов завершён.

Сборка : #${BUILD_NUMBER}
Статус : ${buildStatus}
Ветка  : ${GIT_BRANCH ?: 'N/A'}
Время  : ${new Date()}

${summary}

Полный Allure-отчёт доступен в Jenkins:
${BUILD_URL}allure/

Архив отчёта прикреплён к письму.

---
Jenkins CI | ${JOB_NAME}
"""
                emailext(
                    to                : "${REPORT_RECIPIENT}",
                    subject           : subject,
                    body              : body,
                    attachmentsPattern: 'allure-report.zip',
                    mimeType          : 'text/plain'
                )
            }
        }

        success {
            echo 'Пайплайн завершён успешно.'
        }

        failure {
            echo 'Пайплайн завершился с ошибкой — проверь логи выше.'
        }

        cleanup {
            bat 'if exist allure-report.zip del allure-report.zip'
        }
    }
}