import pytest
from Framework_Core.utils.logUtils.logger import test_logger

def pytest_runtest_setup(item):
    """测试用例开始前的处理"""
    test_logger.info(f"开始执行测试用例: {item.name}")

def pytest_runtest_teardown(item):
    """测试用例结束后的处理"""
    test_logger.info(f"测试用例执行完成: {item.name}")

def pytest_runtest_logreport(report):
    """测试用例执行结果的处理"""
    if report.when == "call":
        if report.passed:
            test_logger.info(f"测试用例通过: {report.nodeid}")
        elif report.failed:
            test_logger.error(f"测试用例失败: {report.nodeid}")
            if hasattr(report, "longrepr"):
                test_logger.error(f"失败原因: {report.longrepr}")
        elif report.skipped:
            test_logger.warning(f"测试用例跳过: {report.nodeid}")

@pytest.fixture(scope="session", autouse=True)
def session_setup_teardown():
    """测试会话的开始和结束处理"""
    test_logger.info("=== 测试会话开始 ===")
    yield
    test_logger.info("=== 测试会话结束 ===")

@pytest.fixture(autouse=True)
def case_setup_teardown():
    """每个测试用例的开始和结束处理"""
    test_logger.info("--- 测试用例开始 ---")
    yield
    test_logger.info("--- 测试用例结束 ---") 