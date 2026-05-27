pipeline {

    agent any

    triggers {
        cron('0 9 * * *')
    }

    environment {

        PYTHON = "C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"

        ALLURE_HOME = tool 'allure'

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

        skipDefaultCheckout(true)

        buildDiscarder(logRotator(numToKeepStr: '10'))

        disableConcurrentBuilds()

        timeout(time: 60, unit: 'MINUTES')

        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Debug Environment') {
            steps {

                powershell """
                    chcp 65001

                    Write-Host "=== WORKSPACE ==="
                    Write-Host "${WORKSPACE}"

                    Write-Host "=== FILES ==="
                    Get-ChildItem

                    Write-Host "=== PYTHON VERSION ==="
                    & "${PYTHON}" --version

                    Write-Host "=== ALLURE VERSION ==="
                    & "${ALLURE_HOME}\\bin\\allure.bat" --version
                """
            }
        }

        stage('Setup Environment') {
            steps {

                echo '=== Установка зависимостей ==='

                dir("${WORKSPACE}") {

                    bat """
                        "${PYTHON}" -m pip install -r requirements.txt

                        "${PYTHON}" -m pip install -e .
                    """

                    echo '=== Очистка старых отчетов ==='

                    bat """
                        if exist allure-results rmdir /s /q allure-results
                        if exist allure-report rmdir /s /q allure-report
                        if exist allure-report.zip del allure-report.zip

                        mkdir allure-results
                    """
                }
            }
        }

        stage('Debug Imports') {
            steps {

                dir("${WORKSPACE}") {

                    powershell """
                        chcp 65001

                        \$env:PYTHONPATH = "${WORKSPACE}"

                        Write-Host "=== PYTHONPATH ==="
                        Write-Host \$env:PYTHONPATH

                        Write-Host "=== IMPORT API ==="
                        & "${PYTHON}" -c "import api; print('api OK')"

                        Write-Host "=== IMPORT UI ==="
                        & "${PYTHON}" -c "import UI; print('UI OK')"

                        Write-Host "=== IMPORT DATABASE ==="
                        & "${PYTHON}" -c "import database; print('DATABASE OK')"

                        Write-Host "=== IMPORT UTILS ==="
                        & "${PYTHON}" -c "import utils; print('UTILS OK')"
                    """
                }
            }
        }

        stage('API Tests') {
            steps {

                echo '=== Запуск API тестов ==='

                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {

                    dir("${WORKSPACE}") {

                        powershell """
                            chcp 65001

                            \$env:PYTHONPATH = "${WORKSPACE}"

                            & "${PYTHON}" -m pytest tests/tests_api `
                                --alluredir=allure-results `
                                --tb=short `
                                -v

                            exit \$LASTEXITCODE
                        """
                    }
                }
            }
        }

        stage('UI Tests') {
            steps {

                echo '=== Запуск UI тестов ==='

                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {

                    dir("${WORKSPACE}") {

                        powershell """
                            chcp 65001

                            \$env:PYTHONPATH = "${WORKSPACE}"

                            & "${PYTHON}" -m pytest tests/tests_ui `
                                --alluredir=allure-results `
                                --tb=short `
                                -v

                            exit \$LASTEXITCODE
                        """
                    }
                }
            }
        }

        stage('Playwright Tests') {
            steps {

                echo '=== Запуск Playwright тестов ==='

                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {

                    dir("${WORKSPACE}") {

                        powershell """
                            chcp 65001

                            \$env:PYTHONPATH = "${WORKSPACE}"

                            & "${PYTHON}" -m pytest tests/tests_ui/playwright_tests `
                                --alluredir=allure-results `
                                --tb=short `
                                -v

                            exit \$LASTEXITCODE
                        """
                    }
                }
            }
        }

        stage('Publish Allure Report') {
            steps {

                echo '=== Публикация Allure отчета ==='

                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }

        stage('Archive Report') {
            steps {

                echo '=== Архивация Allure отчета ==='

                powershell """
                    Compress-Archive `
                        -Path allure-report `
                        -DestinationPath allure-report.zip `
                        -Force
                """

                archiveArtifacts(
                    artifacts: 'allure-report.zip',
                    fingerprint: true
                )
            }
        }
    }

    post {

        always {

            script {

                def buildStatus = currentBuild.currentResult ?: 'UNKNOWN'

                def summary = ''

                def summaryFile = "${ALLURE_REPORT}\\widgets\\summary.json"

                if (fileExists(summaryFile)) {

                    try {

                        def raw = readFile(
                            file: summaryFile,
                            encoding: 'UTF-8'
                        )

                        def json = new groovy.json.JsonSlurper().parseText(raw)

                        def stat = json.statistic

                        summary = """
Результаты тестов:

Passed : ${stat.passed ?: 0}
Failed : ${stat.failed ?: 0}
Broken : ${stat.broken ?: 0}
Skipped: ${stat.skipped ?: 0}
Total  : ${stat.total ?: 0}
"""

                    } catch (e) {

                        summary = "Не удалось прочитать summary.json: ${e}"
                    }

                } else {

                    summary = 'Allure отчет отсутствует'
                }

                def subject = "[Jenkins] Автотесты — ${buildStatus} | Build #${BUILD_NUMBER}"

                def body = """
Автотесты завершены.

Build  : #${BUILD_NUMBER}
Status : ${buildStatus}
Branch : ${env.BRANCH_NAME ?: 'master'}

${summary}

Allure:
${BUILD_URL}allure/

Jenkins Job:
${JOB_NAME}
"""

                emailext(
                    to: "${REPORT_RECIPIENT}",
                    subject: subject,
                    body: body,
                    mimeType: 'text/plain'
                )
            }
        }

        success {
            echo 'PIPELINE SUCCESS'
        }

        failure {
            echo 'PIPELINE FAILURE'
        }

        cleanup {

            bat """
                if exist allure-report.zip del allure-report.zip
            """
        }
    }
}