import csv
import os
from config.config import Config

class CSVDataReader:
    @staticmethod
    def read_csv(file_name):
        """读取CSV文件"""
        file_path = os.path.join(Config.DATA_DIR, file_name)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV文件不存在: {file_path}")
        
        data_list = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_list.append(row)
        return data_list

    @staticmethod
    def get_test_ids(data_list):
        """获取测试用例ID列表"""
        return [item.get("case_id", f"case_{i}") for i, item in enumerate(data_list)]