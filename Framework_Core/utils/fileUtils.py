import os
import yaml
import re
from typing import Dict, Any, List
from Framework_Core.utils.logger import test_logger

class FileUtils:
    def __init__(self):
        self.test_case_dir = "TestSuites/test_cases"
        if not os.path.exists(self.test_case_dir):
            os.makedirs(self.test_case_dir)

    def parse_yaml(self, yaml_path: str) -> Dict[str, Any]:
        """
        解析YAML文件
        :param yaml_path: YAML文件路径
        :return: 解析后的字典
        """
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            test_logger.error(f"解析YAML文件失败: {str(e)}")
            raise

    def _generate_test_case(self, case_data: Dict[str, Any], common_data: Dict[str, Any]) -> str:
        """
        生成单个测试用例代码
        :param case_data: 用例数据
        :param common_data: 公共数据
        :return: 测试用例代码
        """
        # 处理变量替换
        def replace_variables(text: str) -> str:
            if not isinstance(text, str):
                return text
            return re.sub(r'\$\{\{(.*?)\}\}', lambda m: f"self.get_variable('{m.group(1)}')", text)

        # 处理依赖数据
        def process_dependencies(dependencies: List[Dict[str, Any]]) -> str:
            if not dependencies:
                return ""
            
            code = []
            for dep in dependencies:
                case_id = dep.get('case_id')
                for data in dep.get('dependent_data', []):
                    dep_type = data.get('dependent_type')
                    jsonpath = data.get('jsonpath')
                    cache_name = data.get('set_cache')
                    if all([dep_type, jsonpath, cache_name]):
                        code.append(f"        # 获取依赖数据: {case_id}")
                        code.append(f"        dep_response = self.run_dependent_case('{case_id}')")
                        code.append(f"        {cache_name} = self.extract_data(dep_response, '{jsonpath}')")
            return "\n".join(code)

        # 处理断言
        def process_assertions(assertions: Dict[str, Any]) -> str:
            if not assertions:
                return ""
            
            code = []
            for key, assertion in assertions.items():
                jsonpath = assertion.get('jsonpath')
                assert_type = assertion.get('type')
                value = assertion.get('value')
                if all([jsonpath, assert_type, value]):
                    code.append(f"        # 断言: {key}")
                    code.append(f"        actual = self.extract_data(response, '{jsonpath}')")
                    code.append(f"        assert actual {assert_type} {value}, f'断言失败: {{actual}} {assert_type} {value}'")
            return "\n".join(code)

        # 生成测试用例代码
        case_name = case_data.get('detail', 'unnamed_case')
        case_id = list(case_data.keys())[0]
        host = replace_variables(case_data.get('host', ''))
        url = case_data.get('url', '')
        method = case_data.get('method', 'GET')
        headers = case_data.get('headers', {})
        request_type = case_data.get('requestType', 'json')
        data = case_data.get('data', {})
        dependencies = case_data.get('dependence_case_data', [])
        assertions = case_data.get('assert', {})

        # 生成测试用例代码
        code = [
            f"    @allure.title('{case_name}')",
            f"    @allure.severity(allure.severity_level.NORMAL)",
            f"    def test_{case_id}(self):",
            f"        \"\"\"{case_name}\"\"\"",
            f"        test_logger.info(f'开始执行测试用例: {case_name}')",
            "",
            f"        # 准备请求数据",
            f"        url = f'{host}{url}'",
            f"        headers = {headers}",
            f"        data = {data}",
            "",
            process_dependencies(dependencies),
            "",
            f"        # 发送请求",
            f"        test_logger.debug(f'发送{method}请求到: {{url}}')",
            f"        test_logger.debug(f'请求头: {{headers}}')",
            f"        test_logger.debug(f'请求数据: {{data}}')",
            "",
            f"        response = self.api_client.{method.lower()}(",
            f"            url=url,",
            f"            headers=headers,",
        ]

        # 添加请求数据
        if request_type == 'json':
            code.append(f"            json_data=data,")
        elif request_type == 'params':
            code.append(f"            params=data,")
        else:
            code.append(f"            data=data,")

        code.extend([
            f"        )",
            "",
            f"        # 记录响应",
            f"        test_logger.debug(f'响应状态码: {{response.status_code}}')",
            f"        test_logger.debug(f'响应数据: {{response.text}}')",
            "",
            process_assertions(assertions),
            "",
            f"        test_logger.info('测试用例执行完成')",
        ])

        return "\n".join(code)

    def generate_test_file(self, yaml_path: str) -> str:
        """
        生成测试文件
        :param yaml_path: YAML文件路径
        :return: 生成的测试文件路径
        """
        try:
            # 解析YAML
            yaml_data = self.parse_yaml(yaml_path)
            
            # 获取公共数据和用例数据
            common_data = yaml_data.get('case_common', {})
            test_cases = {k: v for k, v in yaml_data.items() if k != 'case_common'}

            # 生成测试文件内容
            file_content = [
                "import pytest",
                "import allure",
                "from typing import Dict, Any",
                "from Framework_Core.extensions.api_plugin import APIRequest",
                "from Framework_Core.utils.logger import test_logger",
                "",
                f"@allure.epic('{common_data.get('allureEpic', '')}')",
                f"@allure.feature('{common_data.get('allureFeature', '')}')",
                f"@allure.story('{common_data.get('allureStory', '')}')",
                "class TestGeneratedCases:",
                "    def __init__(self):",
                "        self.api_client = APIRequest()",
                "",
                "    def get_variable(self, name: str) -> Any:",
                "        \"\"\"获取变量值\"\"\"",
                "        # 这里可以实现变量获取逻辑",
                "        return None",
                "",
                "    def run_dependent_case(self, case_id: str) -> Any:",
                "        \"\"\"运行依赖的测试用例\"\"\"",
                "        # 这里可以实现依赖用例运行逻辑",
                "        return None",
                "",
                "    def extract_data(self, response: Any, jsonpath: str) -> Any:",
                "        \"\"\"从响应中提取数据\"\"\"",
                "        # 这里可以实现数据提取逻辑",
                "        return None",
                "",
            ]

            # 添加测试用例
            for case_id, case_data in test_cases.items():
                if case_data.get('is_run', True):
                    file_content.append(self._generate_test_case({case_id: case_data}, common_data))
                    file_content.append("")

            # 生成测试文件名
            file_name = os.path.splitext(os.path.basename(yaml_path))[0] + "_test.py"
            file_path = os.path.join(self.test_case_dir, file_name)

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(file_content))

            test_logger.info(f"测试用例文件已生成: {file_path}")
            return file_path

        except Exception as e:
            test_logger.error(f"生成测试文件失败: {str(e)}")
            raise 