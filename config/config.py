"""
配置文件
用于管理测试环境的配置信息
"""
import os

class Config:
    """配置类"""
    
    # 基础URL - 优先从环境变量读取，否则使用默认值
    BASE_URL = os.getenv('BASE_URL', 'http://novel.hctestedu.com')
    
    # 测试账号配置
    TEST_USERNAME = os.getenv('TEST_USERNAME', '13754172545')
    TEST_PASSWORD = os.getenv('TEST_PASSWORD', '12345')
    
    # 路径配置
    # 项目根目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 测试数据目录
    DATA_DIR = os.path.join(BASE_DIR, 'test_data')
    
    # 测试报告目录
    REPORT_DIR = os.path.join(BASE_DIR, 'reports')
    
    # Allure报告目录
    ALLURE_RESULTS_DIR = os.path.join(REPORT_DIR, 'allure-results')
    
    # 超时配置
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '10'))
    
    # 重试配置
    MAX_RETRY = int(os.getenv('MAX_RETRY', '3'))
    
    @classmethod
    def get_env_info(cls):
        """获取当前环境信息"""
        return {
            'base_url': cls.BASE_URL,
            'username': cls.TEST_USERNAME,
            'data_dir': cls.DATA_DIR,
            'report_dir': cls.REPORT_DIR
        }
    
    @classmethod
    def print_config(cls):
        """打印配置信息（用于调试）"""
        print("=" * 50)
        print("当前配置信息:")
        print(f"BASE_URL: {cls.BASE_URL}")
        print(f"TEST_USERNAME: {cls.TEST_USERNAME}")
        print(f"DATA_DIR: {cls.DATA_DIR}")
        print(f"REPORT_DIR: {cls.REPORT_DIR}")
        print(f"REQUEST_TIMEOUT: {cls.REQUEST_TIMEOUT}")
        print("=" * 50)


# 环境配置映射
ENV_CONFIGS = {
    'test': {
        'BASE_URL': 'http://novel.hctestedu.com',
        'TEST_USERNAME': '13754172545',
        'TEST_PASSWORD': '12345'
    },
    'staging': {
        'BASE_URL': 'http://novel-staging.hctestedu.com',
        'TEST_USERNAME': '13754172545',
        'TEST_PASSWORD': '12345'
    },
    'prod': {
        'BASE_URL': 'http://novel-prod.hctestedu.com',
        'TEST_USERNAME': '13754172545',
        'TEST_PASSWORD': '12345'
    }
}


def load_env_config(env='test'):
    """
    加载指定环境的配置
    
    Args:
        env: 环境名称 (test/staging/prod)
    """
    if env in ENV_CONFIGS:
        config = ENV_CONFIGS[env]
        for key, value in config.items():
            setattr(Config, key, value)
        print(f"已加载 {env} 环境配置")
    else:
        print(f"未找到环境 {env} 的配置，使用默认配置")


if __name__ == '__main__':
    # 测试配置
    Config.print_config()