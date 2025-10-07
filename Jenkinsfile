pipeline {
    agent any
    
    environment {
        // 环境变量
        BASE_URL = 'http://novel.hctestedu.com'
        TEST_USERNAME = credentials('test-username')
        TEST_PASSWORD = credentials('test-password')
        PYTHON_VERSION = '3.9'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '检出代码...'
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo '设置Python环境...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo '执行测试...'
                sh '''
                    . venv/bin/activate
                    cd project_01
                    pytest tests/ -v --alluredir=reports/allure-results --html=reports/report.html --self-contained-html
                '''
            }
        }
        
        stage('Generate Reports') {
            steps {
                echo '生成测试报告...'
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'project_01/reports/allure-results']]
                    ])
                }
            }
        }
    }
    
    post {
        always {
            echo '清理工作空间...'
            // 发布HTML报告
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'project_01/reports',
                reportFiles: 'report.html',
                reportName: 'Pytest HTML Report'
            ])
            
            // 清理虚拟环境
            sh 'rm -rf venv'
        }
        
        success {
            echo '测试成功！'
            // 可以添加邮件通知
        }
        
        failure {
            echo '测试失败！'
            // 可以添加邮件通知
        }
    }
}