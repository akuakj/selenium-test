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

        stage('Setup Environment') {
            steps {
                dir("${WORKSPACE}") {
                    bat """
                        "${PYTHON}" -m pip install -r requirements.txt
                        "${PYTHON}" -m pip install -e .
                        if exist allure-results rmdir /s /q allure-results
                        if exist allure-report rmdir /s /q allure-report
                        mkdir allure-results
                    """
                }
            }
        }

        stage('API Tests') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    dir("${WORKSPACE}") {
                        powershell """
                            chcp 65001
                            [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
                            \$env:PYTHONPATH = "${WORKSPACE}"

                            & "${PYTHON}" -m pytest tests/tests_api `
                                --alluredir=allure-results `
                                --tb=short -v
                            exit \$LASTEXITCODE
                        """
                    }
                }
            }
        }

        stage('UI Tests') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    dir("${WORKSPACE}") {
                        powershell """
                            chcp 65001
                            \$env:PYTHONPATH = "${WORKSPACE}"
                            & "${PYTHON}" -m pytest tests/tests_ui `
                                --alluredir=allure-results `
                                --tb=short -v
                            exit \$LASTEXITCODE
                        """
                    }
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                dir("${WORKSPACE}") {
                    bat """
                        "${ALLURE_HOME}\\bin\\allure.bat" generate allure-results ^
                            -o allure-report --clean
                    """
                }
                // публикует отчёт в Jenkins UI
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
            script {
                def buildStatus = currentBuild.currentResult ?: 'UNKNOWN'
                def summary = 'Allure отчет не найден'
                def summaryFile = "${ALLURE_REPORT}\\widgets\\summary.json"

                if (fileExists(summaryFile)) {
                    try {
                        def raw  = readFile(file: summaryFile, encoding: 'UTF-8')
                        def json = new groovy.json.JsonSlurper().parseText(raw)
                        def s    = json.statistic

                        summary = """\
Passed : ${s.passed  ?: 0}
Failed : ${s.failed  ?: 0}
Broken : ${s.broken  ?: 0}
Skipped: ${s.skipped ?: 0}
Total  : ${s.total   ?: 0}"""

                    } catch (e) {
                        summary = "Ошибка чтения summary.json: ${e}"
                    }
                }

                emailext(
                    to: "${REPORT_RECIPIENT}",
                    subject: "[Jenkins] Автотесты — ${buildStatus} | Build #${BUILD_NUMBER}",
                    body: """\
Автотесты завершены.

Build  : #${BUILD_NUMBER}
Status : ${buildStatus}
Branch : ${env.BRANCH_NAME ?: 'master'}

Результаты:
${summary}

Allure отчет: ${BUILD_URL}allure/
""",
                    mimeType: 'text/plain'
                )
            }
        }

        success { echo 'PIPELINE SUCCESS' }
        failure { echo 'PIPELINE FAILURE' }
    }
}