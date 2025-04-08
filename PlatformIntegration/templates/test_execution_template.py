import pytest
from typing import Dict, Any
from PlatformIntegration.api.platform_api import PlatformAPI
from Framework_Core.utils.config_loader import ConfigLoader

class TestExecutionTemplate:
    def __init__(self):
        self.platform_api = PlatformAPI()
        self.config_loader = ConfigLoader()
        self.execution_id = None

    def setup_suite(self, suite_name: str, env: str = 'test'):
        """
        设置测试套件
        :param suite_name: 套件名称
        :param env: 环境名称
        """
        # 启动测试执行
        self.execution_id = self.platform_api.start_test_execution(suite_name, env)
        
        # 获取环境配置
        env_config = self.platform_api.get_test_environment(env)
        if env_config:
            # 更新配置
            self.config_loader.update_config('test_environment', env_config)

    def teardown_suite(self, results: Dict[str, Any]):
        """
        清理测试套件
        :param results: 测试结果
        """
        if self.execution_id:
            # 计算测试状态
            status = 'PASSED' if results.get('failed', 0) == 0 else 'FAILED'
            
            # 完成测试执行
            self.platform_api.complete_test_execution(
                self.execution_id,
                status,
                results
            )

            # 上传测试报告
            self.platform_api.upload_test_artifacts(
                self.execution_id,
                {
                    'allure': './allure-report',
                    'logs': './logs/test_execution.log'
                }
            )

    @pytest.fixture(scope="session", autouse=True)
    def manage_test_execution(self, request):
        """
        管理测试执行的fixture
        """
        # 设置套件
        self.setup_suite('example_suite')
        
        def finalize():
            # 获取测试结果
            results = {
                'total': request.session.testscollected,
                'passed': request.session.testspassed,
                'failed': request.session.testsfailed,
                'skipped': request.session.testsskipped,
                'duration': request.session.duration
            }
            # 清理套件
            self.teardown_suite(results)
            
        request.addfinalizer(finalize)

    @pytest.fixture(autouse=True)
    def manage_test_case(self, request):
        """
        管理测试用例的fixture
        """
        test_case = request.node
        case_id = f"{test_case.module.__name__}.{test_case.name}"
        
        # 更新用例状态为运行中
        self.platform_api.update_test_case_status(case_id, 'RUNNING')
        
        def finalize():
            # 根据测试结果更新状态
            if test_case.passed:
                status = 'PASSED'
            elif test_case.failed:
                status = 'FAILED'
            else:
                status = 'SKIPPED'
            
            # 更新用例状态
            self.platform_api.update_test_case_status(
                case_id,
                status,
                str(getattr(test_case, '_excinfo', None))
            )
            
        request.addfinalizer(finalize)

# 使用示例
"""
from PlatformIntegration.templates.test_execution_template import TestExecutionTemplate

class TestExample(TestExecutionTemplate):
    def test_something(self):
        assert True

    def test_another_thing(self):
        assert True
""" 