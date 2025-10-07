import requests
import pytest
import json
import os
from faker import Faker
import allure
import csv
fake = Faker("zh_CN")
base_url = "http://novel.hctestedu.com"

@pytest.fixture(scope="session")
def get_token():
    url = f"{base_url}/user/login"
    data = {
        'username' : '13754172545',
        'password' : '12345'
    }
    res = requests.post(url,params=data)
    ans = res.json()
    token = ans.get("data").get("token")
    assert res.status_code == 200
    return token

@pytest.fixture(scope="session")
def header(get_token):
    return {"Authorization" : get_token}


def test_rank(header):
    url = f"{base_url}/book/listRank"
    data = {
        "type": "3",
        "limit": "1"
    }
    
    res = requests.get(url,params=data,headers=header)
    ans = res.json()
    assert ans.get('code') == '200'



@allure.feature("用户模块")
@allure.story("用户登录")
class TestLogin:
    
    @pytest.mark.parametrize("test_data", 
                            CSVDataReader.read_csv('login_test_data.csv'),
                            ids=CSVDataReader.get_test_ids(CSVDataReader.read_csv('login_test_data.csv')))
    def test_login(self, test_data):
        """登录接口数据驱动测试"""
        with allure.step(f"执行用例: {test_data.get('case_name')}"):
            allure.dynamic.title(test_data.get('case_name'))
            allure.dynamic.description(test_data.get('description'))
            
            # 构建请求数据
            url = f"{base_url}/user/login"
            params = {
                'username': test_data.get('username'),
                'password': test_data.get('password')
            }
            
            allure.attach(str(params), "请求参数", allure.attachment_type.JSON)
            
            # 发送请求
            res = requests.post(url, params=params)
            ans = res.json()
            
            allure.attach(res.text, "响应数据", allure.attachment_type.JSON)
        
        with allure.step("验证响应结果"):
            expected_code = test_data.get('expected_code')
            actual_code = ans.get('code')
            
            assert str(actual_code) == str(expected_code), \
                f"预期code: {expected_code}, 实际code: {actual_code}, 消息: {ans.get('msg')}"
            
            # 如果需要验证其他字段
            if test_data.get('check_token') == 'true':
                assert ans.get('data', {}).get('token') is not None, "token不存在"



@allure.feature("排行榜模块")
@allure.story("排行榜查询")
class TestBookQuery:
    
    @pytest.mark.parametrize("test_data",
                            CSVDataReader.read_csv('book_range_test_data.csv'),
                            ids=CSVDataReader.get_test_ids(CSVDataReader.read_csv('book_range_test_data.csv')))
    def test_book_query(self, header, test_data):
        """排行榜查询接口数据驱动测试"""
        with allure.step(f"执行用例: {test_data.get('case_name')}"):
            allure.dynamic.title(test_data.get('case_name'))
            
            url = f"{base_url}/book/listRank"
            
            # 构建查询参数
            params = {}
            if test_data.get('type'):
                params['type'] = test_data.get('type')
            if test_data.get('limit'):
                params['limit'] = test_data.get('limit')
            
            allure.attach(str(params), "请求参数", allure.attachment_type.JSON)
            
            # 发送请求
            res = requests.get(url, params=params, headers=header)
            ans = res.json()
            
            allure.attach(res.text, "响应数据", allure.attachment_type.JSON)
        
        with allure.step("验证响应结果"):
            expected_code = test_data.get('expected_code')
            assert str(ans.get('code')) == str(expected_code), \
                f"预期code: {expected_code}, 实际: {ans.get('code')}"
        



@allure.feature("作家专区")
@allure.story("书籍管理")
class TestAuthorBook:
    
    @pytest.mark.parametrize("test_data",
                            CSVDataReader.read_csv('author_addbook_test_data.csv'),
                            ids=CSVDataReader.get_test_ids(CSVDataReader.read_csv('author_addbook_test_data.csv')))
    def test_add_book(self, header, test_data):
        """新增书籍接口数据驱动测试"""
        with allure.step(f"执行用例: {test_data.get('case_name')}"):
            allure.dynamic.title(test_data.get('case_name'))
            allure.dynamic.severity(test_data.get('severity'))
            
            url = f"{base_url}/author/addBook"
            
            # 构建请求数据
            data = {
                'workDirection': test_data.get('workDirection'),
                'catId': test_data.get('catId'),
                'catName': test_data.get('catName'),
                'bookName': test_data.get('bookName'),
                'picUrl': test_data.get('picUrl', ''),
                'bookDesc': test_data.get('bookDesc')
            }
            
            allure.attach(str(data), "请求参数", allure.attachment_type.JSON)

            # 发送请求
            if test_data.get("if_have_token") == "TRUE":
                res = requests.post(url, data=data, headers=header)
            else:
                res = requests.post(url, data=data)
            ans = res.json()
            
            
            allure.attach(res.text, "响应数据", allure.attachment_type.JSON)
        
        with allure.step("验证响应结果"):
            expected_code = test_data.get('expected_code')
            actual_code = ans.get('code')
            
            assert str(actual_code) == str(expected_code), \
                f"预期code: {expected_code}, 实际: {actual_code}, 消息: {ans.get('msg')}"
