[pytest]
# 测试目录
testpaths = project_01/tests

# 测试文件命名规则
python_files = test_*.py

# 测试类命名规则
python_classes = Test*

# 测试函数命名规则
python_functions = test_*

# 命令行参数
addopts = -v 
          --tb=short
          --strict-markers
          --alluredir=project_01/reports/allure-results
          --html=project_01/reports/report.html
          --self-contained-html

# 标记
markers =
    smoke: 冒烟测试
    regression: 回归测试
    slow: 慢速测试