import os
import subprocess
from typing import Optional
from loguru import logger

class AllureReporter:
    def __init__(self, results_dir: str = "./allure-results", report_dir: str = "./allure-report"):
        self.results_dir = results_dir
        self.report_dir = report_dir

    def generate_report(self) -> bool:
        """
        生成Allure报告
        :return: 是否成功生成报告
        """
        try:
            if not os.path.exists(self.results_dir):
                logger.error(f"结果目录不存在: {self.results_dir}")
                return False

            # 生成报告
            cmd = f"allure generate {self.results_dir} -o {self.report_dir} --clean"
            subprocess.run(cmd, shell=True, check=True)
            logger.info(f"报告已生成到: {self.report_dir}")
            return True
        except Exception as e:
            logger.error(f"生成报告失败: {str(e)}")
            return False

    def serve_report(self, port: int = 8080) -> Optional[subprocess.Popen]:
        """
        启动Allure报告服务
        :param port: 服务端口
        :return: 服务进程对象
        """
        try:
            cmd = f"allure serve -p {port} {self.results_dir}"
            process = subprocess.Popen(cmd, shell=True)
            logger.info(f"报告服务已启动在端口: {port}")
            return process
        except Exception as e:
            logger.error(f"启动报告服务失败: {str(e)}")
            return None

    @staticmethod
    def clean_results(results_dir: str) -> bool:
        """
        清理测试结果目录
        :param results_dir: 结果目录路径
        :return: 是否成功清理
        """
        try:
            if os.path.exists(results_dir):
                for file in os.listdir(results_dir):
                    file_path = os.path.join(results_dir, file)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
            logger.info(f"已清理结果目录: {results_dir}")
            return True
        except Exception as e:
            logger.error(f"清理结果目录失败: {str(e)}")
            return False 