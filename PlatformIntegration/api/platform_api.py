from typing import Dict, Any, List, Optional
import os
from datetime import datetime
from Framework_Core.utils.platform_adapter import PlatformAdapter
from Framework_Core.utils.config_loader import ConfigLoader
from loguru import logger

class PlatformAPI:
    def __init__(self):
        self.config_loader = ConfigLoader()
        platform_config = self.config_loader.get_value('platform', {})
        self.adapter = PlatformAdapter(platform_config)
        self.project_id = platform_config.get('project_id')

    def start_test_execution(self, suite_name: str, env: str) -> Optional[str]:
        """
        启动测试执行
        :param suite_name: 测试套件名称
        :param env: 执行环境
        :return: 执行ID
        """
        try:
            execution_data = {
                'project_id': self.project_id,
                'suite_name': suite_name,
                'environment': env,
                'start_time': datetime.now().isoformat(),
                'status': 'RUNNING'
            }
            self.adapter.notify_execution_status(execution_data['id'], 'RUNNING')
            return execution_data['id']
        except Exception as e:
            logger.error(f"启动测试执行失败: {str(e)}")
            return None

    def complete_test_execution(self, execution_id: str, status: str, results: Dict[str, Any]) -> bool:
        """
        完成测试执行
        :param execution_id: 执行ID
        :param status: 执行状态
        :param results: 执行结果
        :return: 是否成功
        """
        try:
            # 上传测试结果
            if not self.adapter.upload_test_results(results):
                return False

            # 更新执行状态
            completion_data = {
                'end_time': datetime.now().isoformat(),
                'status': status
            }
            return self.adapter.notify_execution_status(execution_id, status, str(results.get('summary', '')))
        except Exception as e:
            logger.error(f"完成测试执行失败: {str(e)}")
            return False

    def sync_test_cases_to_platform(self, test_cases: List[Dict[str, Any]]) -> bool:
        """
        同步测试用例到平台
        :param test_cases: 测试用例列表
        :return: 是否同步成功
        """
        try:
            return self.adapter.sync_test_cases(test_cases)
        except Exception as e:
            logger.error(f"同步测试用例失败: {str(e)}")
            return False

    def upload_test_artifacts(self, execution_id: str, artifacts: Dict[str, str]) -> bool:
        """
        上传测试产物
        :param execution_id: 执行ID
        :param artifacts: 产物字典 {类型: 路径}
        :return: 是否上传成功
        """
        try:
            success = True
            for artifact_type, path in artifacts.items():
                if os.path.exists(path):
                    if not self.adapter.upload_report(path, artifact_type):
                        success = False
                else:
                    logger.warning(f"产物文件不存在: {path}")
                    success = False
            return success
        except Exception as e:
            logger.error(f"上传测试产物失败: {str(e)}")
            return False

    def get_test_environment(self, env: str) -> Optional[Dict[str, Any]]:
        """
        获取测试环境配置
        :param env: 环境名称
        :return: 环境配置
        """
        try:
            return self.adapter.get_environment_variables(env)
        except Exception as e:
            logger.error(f"获取测试环境配置失败: {str(e)}")
            return None

    def update_test_case_status(self, case_id: str, status: str, message: str = None) -> bool:
        """
        更新测试用例状态
        :param case_id: 用例ID
        :param status: 状态
        :param message: 状态信息
        :return: 是否更新成功
        """
        try:
            return self.adapter.update_test_status(case_id, status)
        except Exception as e:
            logger.error(f"更新测试用例状态失败: {str(e)}")
            return False

    def get_suite_config(self, suite_name: str) -> Optional[Dict[str, Any]]:
        """
        获取测试套件配置
        :param suite_name: 套件名称
        :return: 套件配置
        """
        try:
            return self.adapter.get_test_config(f"suite_{suite_name}")
        except Exception as e:
            logger.error(f"获取测试套件配置失败: {str(e)}")
            return None 