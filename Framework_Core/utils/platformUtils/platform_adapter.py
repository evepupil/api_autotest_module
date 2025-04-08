from typing import Dict, Any, List, Optional
import requests
from loguru import logger
from .config_loader import ConfigLoader

class PlatformAdapter:
    def __init__(self, platform_config: Dict[str, Any]):
        """
        初始化平台适配器
        :param platform_config: 平台配置
        """
        self.config = platform_config
        self.base_url = platform_config.get('api_base_url', '')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {platform_config.get('api_token', '')}"
        }

    def upload_test_results(self, results: Dict[str, Any]) -> bool:
        """
        上传测试结果到平台
        :param results: 测试结果数据
        :return: 是否上传成功
        """
        try:
            url = f"{self.base_url}/api/test-results"
            response = requests.post(url, json=results, headers=self.headers)
            response.raise_for_status()
            logger.info("测试结果上传成功")
            return True
        except Exception as e:
            logger.error(f"上传测试结果失败: {str(e)}")
            return False

    def update_test_status(self, test_id: str, status: str) -> bool:
        """
        更新测试状态
        :param test_id: 测试ID
        :param status: 测试状态
        :return: 是否更新成功
        """
        try:
            url = f"{self.base_url}/api/tests/{test_id}/status"
            response = requests.put(url, json={'status': status}, headers=self.headers)
            response.raise_for_status()
            logger.info(f"测试状态更新成功: {test_id} -> {status}")
            return True
        except Exception as e:
            logger.error(f"更新测试状态失败: {str(e)}")
            return False

    def get_test_config(self, test_id: str) -> Optional[Dict[str, Any]]:
        """
        从平台获取测试配置
        :param test_id: 测试ID
        :return: 测试配置
        """
        try:
            url = f"{self.base_url}/api/tests/{test_id}/config"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"获取测试配置失败: {str(e)}")
            return None

    def sync_test_cases(self, test_cases: List[Dict[str, Any]]) -> bool:
        """
        同步测试用例到平台
        :param test_cases: 测试用例列表
        :return: 是否同步成功
        """
        try:
            url = f"{self.base_url}/api/test-cases/sync"
            response = requests.post(url, json={'test_cases': test_cases}, headers=self.headers)
            response.raise_for_status()
            logger.info("测试用例同步成功")
            return True
        except Exception as e:
            logger.error(f"同步测试用例失败: {str(e)}")
            return False

    def upload_report(self, report_path: str, report_type: str = 'allure') -> bool:
        """
        上传测试报告到平台
        :param report_path: 报告文件路径
        :param report_type: 报告类型
        :return: 是否上传成功
        """
        try:
            url = f"{self.base_url}/api/reports"
            with open(report_path, 'rb') as f:
                files = {'file': f}
                data = {'type': report_type}
                response = requests.post(url, files=files, data=data, headers=self.headers)
            response.raise_for_status()
            logger.info("测试报告上传成功")
            return True
        except Exception as e:
            logger.error(f"上传测试报告失败: {str(e)}")
            return False

    def notify_execution_status(self, execution_id: str, status: str, message: str = None) -> bool:
        """
        通知执行状态
        :param execution_id: 执行ID
        :param status: 执行状态
        :param message: 状态信息
        :return: 是否通知成功
        """
        try:
            url = f"{self.base_url}/api/executions/{execution_id}/status"
            data = {
                'status': status,
                'message': message
            }
            response = requests.put(url, json=data, headers=self.headers)
            response.raise_for_status()
            logger.info(f"执行状态通知成功: {execution_id} -> {status}")
            return True
        except Exception as e:
            logger.error(f"通知执行状态失败: {str(e)}")
            return False

    def get_environment_variables(self, env: str) -> Optional[Dict[str, str]]:
        """
        获取环境变量
        :param env: 环境名称
        :return: 环境变量字典
        """
        try:
            url = f"{self.base_url}/api/environments/{env}/variables"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"获取环境变量失败: {str(e)}")
            return None 