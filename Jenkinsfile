pipeline {
  agent any

  environment {
    BASE_URL = 'http://novel.hctestedu.com'
    TEST_USERNAME = '13754172545'
    TEST_PASSWORD = '12345'
  }

  options {
    timestamps()
    ansiColor('xterm')
  }

  stages {
    stage('Checkout') {
      steps {
        echo '检出代码...'
        checkout scm
        bat 'dir'
      }
    }

    stage('Setup Python venv') {
      steps {
        echo '创建虚拟环境并安装依赖...'
        bat '''
        py -3 -m venv venv
        call venv\\Scripts\\activate
        python --version
        pip install --upgrade pip
        pip install -r requirements.txt
        '''
      }
    }

    stage('Run Pytest') {
      steps {
        echo '执行 Pytest...'
        bat '''
        call venv\\Scripts\\activate
        pytest -q --alluredir=allure-results
        '''
      }
    }

    stage('Archive & Allure') {
      steps {
        archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
        // 先在 Jenkins 安装 Allure Jenkins 插件
        allure([
          includeProperties: false,
          jdk: '',
          results: [[path: 'allure-results']]
        ])
      }
    }
  }

  post {
    success { echo '测试执行完成 ✅' }
    failure { echo '测试失败 ❌（看上面的报错）' }
  }
}
