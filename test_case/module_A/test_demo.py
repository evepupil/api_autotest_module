import pytest
import allure
import json
from typing import Dict
from Framework_Core.utils.requestUtils.api_plugin import APIRequest
from Framework_Core.utils.logUtils.logger import test_logger

@pytest.fixture(scope="module")
def api_client():
    """创建API客户端实例"""
    test_logger.info("初始化API客户端")
    client = APIRequest(base_url="https://api.example.com")
    client.set_headers({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    test_logger.debug(f"API客户端headers设置: {client.session.headers}")
    return client

@pytest.fixture
def test_data() -> Dict:
    """加载测试数据"""
    test_logger.info("加载测试数据")
    with open("Resources/test_data/demo_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        test_logger.debug(f"加载的测试数据: {data}")
        return data

@allure.feature("示例模块")
@allure.story("用户管理")
class TestUserManagement:
    
    @allure.title("测试创建用户")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("user_data", [
        {"username": "test_user1", "email": "test1@example.com"},
        {"username": "test_user2", "email": "test2@example.com"}
    ])
    def test_create_user(self, api_client: APIRequest, user_data: Dict):
        """测试创建用户接口"""
        test_logger.info(f"开始测试创建用户: {user_data}")
        
        with allure.step("发送创建用户请求"):
            test_logger.debug(f"发送创建用户请求，数据: {user_data}")
            response = api_client.post("/users", json_data=user_data)
            test_logger.debug(f"创建用户响应状态码: {response.status_code}")
            test_logger.debug(f"创建用户响应数据: {response.text}")
        
        with allure.step("验证响应状态码"):
            assert response.status_code == 201, f"创建用户失败: {response.text}"
            test_logger.info("响应状态码验证通过")
        
        with allure.step("验证响应数据"):
            resp_data = response.json()
            test_logger.debug(f"验证响应数据: {resp_data}")
            assert resp_data["username"] == user_data["username"]
            assert resp_data["email"] == user_data["email"]
            assert "id" in resp_data
            test_logger.info("响应数据验证通过")

    @allure.title("测试获取用户信息")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user(self, api_client: APIRequest, test_data: Dict):
        """测试获取用户信息接口"""
        user_id = test_data["existing_user_id"]
        test_logger.info(f"开始测试获取用户信息，用户ID: {user_id}")
        
        with allure.step(f"获取用户ID: {user_id}的信息"):
            test_logger.debug(f"发送获取用户信息请求，用户ID: {user_id}")
            response = api_client.get(f"/users/{user_id}")
            test_logger.debug(f"获取用户信息响应状态码: {response.status_code}")
            test_logger.debug(f"获取用户信息响应数据: {response.text}")
        
        with allure.step("验证响应状态码"):
            assert response.status_code == 200, f"获取用户信息失败: {response.text}"
            test_logger.info("响应状态码验证通过")
        
        with allure.step("验证响应数据"):
            resp_data = response.json()
            test_logger.debug(f"验证响应数据: {resp_data}")
            assert resp_data["id"] == user_id
            assert "username" in resp_data
            assert "email" in resp_data
            test_logger.info("响应数据验证通过")

    @allure.title("测试更新用户信息")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user(self, api_client: APIRequest, test_data: Dict):
        """测试更新用户信息接口"""
        user_id = test_data["existing_user_id"]
        update_data = {
            "email": "updated@example.com"
        }
        test_logger.info(f"开始测试更新用户信息，用户ID: {user_id}")
        test_logger.debug(f"更新数据: {update_data}")
        
        with allure.step(f"更新用户ID: {user_id}的信息"):
            test_logger.debug(f"发送更新用户信息请求，用户ID: {user_id}")
            response = api_client.put(f"/users/{user_id}", json_data=update_data)
            test_logger.debug(f"更新用户信息响应状态码: {response.status_code}")
            test_logger.debug(f"更新用户信息响应数据: {response.text}")
        
        with allure.step("验证响应状态码"):
            assert response.status_code == 200, f"更新用户信息失败: {response.text}"
            test_logger.info("响应状态码验证通过")
        
        with allure.step("验证响应数据"):
            resp_data = response.json()
            test_logger.debug(f"验证响应数据: {resp_data}")
            assert resp_data["id"] == user_id
            assert resp_data["email"] == update_data["email"]
            test_logger.info("响应数据验证通过") 