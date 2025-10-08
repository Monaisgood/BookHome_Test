pipeline {
  agent any

  environment {
    // 你的测试会读取这些变量（也可删掉，用 config.py 的默认值）
    BASE_URL      = 'http://novel.hctestedu.com'
    TEST_USERNAME = '13754172545'
    TEST_PASSWORD = '12345'
    // 解决中文输出乱码
    PYTHONIOENCODING = 'utf-8'
  }

  options {
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps {
        echo '检出代码...'
        checkout scm
        // 看看目录结构（排查很有用）
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
        // 产出两类报告：Allure 原始数据 + JUnit XML
        bat '''
        call venv\\Scripts\\activate
        pytest -q --alluredir=allure-results --junitxml=reports\\junit.xml
        '''
      }
    }
  }

  post {
    // ✅ 不论成功还是失败，都会执行这里
    always {
      echo '发布测试报告（不论成功/失败）...'
      // 归档产物（构建制品里可下载）
      archiveArtifacts artifacts: 'allure-results/**, reports/**', allowEmptyArchive: true

      // 发布 JUnit（Jenkins 自带测试趋势）
      // 没有就忽略，不会阻断
      script {
        try {
          junit 'reports/**/*.xml'
        } catch (ignored) {
          echo 'JUnit 报告未找到或解析失败，已跳过。'
        }
      }

      // 发布 Allure（需要已安装 Allure Jenkins 插件）
      // 若插件未安装，不要让流水线失败
      script {
        try {
          allure([
            includeProperties: false,
            jdk: '',
            results: [[path: 'allure-results']]
          ])
        } catch (ignored) {
          echo 'Allure 插件未安装或执行出错，已跳过发布。'
        }
      }
    }

    success {
      echo '测试执行完成 ✅'
    }
    failure {
      echo '测试失败 ❌（报告已发布，请在 Allure/JUnit 查看详情）'
    }
  }
}
