import os

class Config:
    # 基础URL
    BASE_URL = os.getenv('BASE_URL', 'http://novel.hctestedu.com')
    
    # 测试账号
    TEST_USERNAME = os.getenv('TEST_USERNAME', '13754172545')
    TEST_PASSWORD = os.getenv('TEST_PASSWORD', '12345')
    
    # 数据目录
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_data')
    
    # 报告目录
    REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')