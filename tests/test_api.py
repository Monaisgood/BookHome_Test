import requests
import pytest
import allure
import sys
import os

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.csv_reader import CSVDataReader
from config.config import Config


class TestBase:
    """测试基类"""
    base_url = Config.BASE_URL


@pytest.fixture(scope="session")
def get_token():
    """获取登录token的fixture"""
    url = f"{Config.BASE_URL}/user/login"
    data = {
        'username': Config.TEST_USERNAME,
        'password': Config.TEST_PASSWORD
    }
    
    with allure.step(f"登录获取token - 用户名: {Config.TEST_USERNAME}"):
        res = requests.post(url, params=data)
        ans = res.json()
        
        assert res.status_code == 200, f"登录请求失败，状态码: {res.status_code}"
        assert ans.get("code") == "200", f"登录失败: {ans.get('msg')}"
        
        token = ans.get("data", {}).get("token")
        assert token is not None, "token获取失败"
        
        allure.attach(token, "Token", allure.attachment_type.TEXT)
        return token


@pytest.fixture(scope="session")
def header(get_token):
    """构造请求头的fixture"""
    return {"Authorization": get_token}


@allure.feature("接口健康检查")
@allure.story("基础功能验证")
class TestHealthCheck(TestBase):
    """健康检查测试"""
    
    @allure.title("验证排行榜接口可用性")
    @allure.description("快速验证核心接口是否正常工作")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_rank(self, header):
        """测试排行榜接口"""
        url = f"{self.base_url}/book/listRank"
        data = {
            "type": "0",
            "limit": "1"
        }
        
        with allure.step("发送排行榜查询请求"):
            res = requests.get(url, params=data, headers=header)
            ans = res.json()
            
            allure.attach(str(data), "请求参数", allure.attachment_type.JSON)
            allure.attach(res.text, "响应数据", allure.attachment_type.JSON)
        
        with allure.step("验证响应结果"):
            assert res.status_code == 200, f"请求失败，状态码: {res.status_code}"
            assert ans.get('code') == '200', f"接口返回异常: {ans.get('msg')}"


@allure.feature("用户模块")
@allure.story("用户登录")
class TestLogin(TestBase):
    """用户登录测试类"""
    
    @pytest.mark.parametrize(
        "test_data",
        CSVDataReader.read_csv('login_test_data.csv'),
        ids=CSVDataReader.get_test_ids(CSVDataReader.read_csv('login_test_data.csv'))
    )
    def test_login(self, test_data):
        """登录接口数据驱动测试"""
        
        with allure.step(f"执行用例: {test_data.get('case_name')}"):
            # 动态设置用例信息
            allure.dynamic.title(test_data.get('case_name'))
            allure.dynamic.description(test_data.get('description', ''))
            allure.dynamic.severity(test_data.get('severity', 'normal'))
            
            # 构建请求数据
            url = f"{self.base_url}/user/login"
            params = {
                'username': test_data.get('username', ''),
                'password': test_data.get('password', '')
            }
            
            allure.attach(str(params), "请求参数", allure.attachment_type.JSON)
        
        with allure.step("发送登录请求"):
            try:
                res = requests.post(url, params=params, timeout=10)
                ans = res.json()
                allure.attach(res.text, "响应数据", allure.attachment_type.JSON)
            except requests.exceptions.RequestException as e:
                pytest.fail(f"请求异常: {str(e)}")
        
        with allure.step("验证响应结果"):
            expected_code = test_data.get('expected_code')
            actual_code = ans.get('code')
            
            # 断言状态码
            assert str(actual_code) == str(expected_code), \
                f"预期code: {expected_code}, 实际code: {actual_code}, 消息: {ans.get('msg')}"
            
            # 如果需要验证token
            if test_data.get('check_token', '').lower() == 'true':
                token = ans.get('data', {}).get('token')
                assert token is not None and token != '', "token不存在或为空"
                allure.attach(token, "返回的Token", allure.attachment_type.TEXT)


@allure.feature("书籍模块")
@allure.story("排行榜查询")
class TestBookQuery(TestBase):
    """书籍查询测试类"""
    
    @pytest.mark.parametrize(
        "test_data",
        CSVDataReader.read_csv('book_range_test_data.csv'),
        ids=CSVDataReader.get_test_ids(CSVDataReader.read_csv('book_range_test_data.csv'))
    )
    def test_book_query(self, header, test_data):
        """排行榜查询接口数据驱动测试"""
        
        with allure.step(f"执行用例: {test_data.get('case_name')}"):
            allure.dynamic.title(test_data.get('case_name'))
            allure.dynamic.description(test_data.get('description', ''))
            allure.dynamic.severity(test_data.get('severity', 'normal'))
            
            url = f"{self.base_url}/book/listRank"
            
            # 构建查询参数
            params = {}
            if test_data.get('type'):
                params['type'] = test_data.get('type')
            if test_data.get('limit'):
                params['limit'] = test_data.get('limit')
            
            allure.attach(str(params), "请求参数", allure.attachment_type.JSON)
        
        with allure.step("发送查询请求"):
            try:
                res = requests.get(url, params=params, headers=header, timeout=10)
                ans = res.json()
                allure.attach(res.text, "响应数据", allure.attachment_type.JSON)
            except requests.exceptions.RequestException as e:
                pytest.fail(f"请求异常: {str(e)}")
        
        with allure.step("验证响应结果"):
            expected_code = test_data.get('expected_code')
            actual_code = ans.get('code')
            
            assert str(actual_code) == str(expected_code), \
                f"预期code: {expected_code}, 实际: {actual_code}, 消息: {ans.get('msg')}"
            
            # 如果成功，验证返回数据结构
            if str(actual_code) == '200':
                assert 'data' in ans, "响应中缺少data字段"
                data = ans.get('data')
                if data:  # 如果有数据
                    assert isinstance(data, list), "data字段应该是列表类型"
                    allure.attach(f"返回数据条数: {len(data)}", "数据统计", allure.attachment_type.TEXT)


@allure.feature("作家专区")
@allure.story("书籍管理")
class TestAuthorBook(TestBase):
    """作家书籍管理测试类"""
    
    @pytest.mark.parametrize(
        "test_data",
        CSVDataReader.read_csv('author_addbook_test_data.csv'),
        ids=CSVDataReader.get_test_ids(CSVDataReader.read_csv('author_addbook_test_data.csv'))
    )
    def test_add_book(self, header, test_data):
        """新增书籍接口数据驱动测试"""
        
        with allure.step(f"执行用例: {test_data.get('case_name')}"):
            allure.dynamic.title(test_data.get('case_name'))
            allure.dynamic.description(test_data.get('description', ''))
            allure.dynamic.severity(test_data.get('severity', 'normal'))
            
            url = f"{self.base_url}/author/addBook"
            
            # 构建请求数据
            data = {
                'workDirection': test_data.get('workDirection', ''),
                'catId': test_data.get('catId', ''),
                'catName': test_data.get('catName', ''),
                'bookName': test_data.get('bookName', ''),
                'picUrl': test_data.get('picUrl', ''),
                'bookDesc': test_data.get('bookDesc', '')
            }
            
            allure.attach(str(data), "请求参数", allure.attachment_type.JSON)
        
        with allure.step("发送添加书籍请求"):
            try:
                # 根据测试数据决定是否带token
                if test_data.get("if_have_token", "").upper() == "TRUE":
                    res = requests.post(url, data=data, headers=header, timeout=10)
                else:
                    res = requests.post(url, data=data, timeout=10)
                
                ans = res.json()
                allure.attach(res.text, "响应数据", allure.attachment_type.JSON)
            except requests.exceptions.RequestException as e:
                pytest.fail(f"请求异常: {str(e)}")
        
        with allure.step("验证响应结果"):
            expected_code = test_data.get('expected_code')
            actual_code = ans.get('code')
            
            assert str(actual_code) == str(expected_code), \
                f"预期code: {expected_code}, 实际: {actual_code}, 消息: {ans.get('msg')}"
            
            # 如果是成功的用例，记录书籍ID
            if str(actual_code) == '200' and ans.get('data'):
                book_id = ans.get('data', {}).get('id')
                if book_id:
                    allure.attach(str(book_id), "创建的书籍ID", allure.attachment_type.TEXT)


@allure.feature("书籍模块")
@allure.story("书籍详情查询")
class TestBookDetail(TestBase):
    """书籍详情测试类"""
    
    @allure.title("查询书籍详情")
    @allure.description("通过书籍ID查询详细信息")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_query_book_detail(self, header):
        """查询书籍详情接口测试"""
        
        # 先获取一本书的ID
        with allure.step("获取书籍列表"):
            list_url = f"{self.base_url}/book/listRank"
            list_res = requests.get(list_url, params={"type": "0", "limit": "1"}, headers=header)
            list_ans = list_res.json()
            
            assert list_ans.get('code') == '200', "获取书籍列表失败"
            books = list_ans.get('data', [])
            assert len(books) > 0, "书籍列表为空"
            
            book_id = books[0].get('id')
            allure.attach(str(book_id), "测试书籍ID", allure.attachment_type.TEXT)
        
        with allure.step(f"查询书籍详情 - ID: {book_id}"):
            detail_url = f"{self.base_url}/book/queryBookDetail/{book_id}"
            res = requests.get(detail_url, headers=header)
            ans = res.json()
            
            allure.attach(res.text, "响应数据", allure.attachment_type.JSON)
        
        with allure.step("验证响应结果"):
            assert res.status_code == 200, f"请求失败，状态码: {res.status_code}"
            assert ans.get('code') == '200', f"接口返回异常: {ans.get('msg')}"
            
            # 验证必要字段
            data = ans.get('data', {})
            assert data.get('id') == book_id, "返回的书籍ID不匹配"
            assert data.get('bookName'), "书籍名称不能为空"
            assert data.get('authorName'), "作者名称不能为空"


if __name__ == '__main__':
    # 本地运行测试
    pytest.main([
        __file__,
        '-v',
        '-s',
        '--alluredir=../reports/allure-results',
        '--html=../reports/report.html',
        '--self-contained-html'
    ])