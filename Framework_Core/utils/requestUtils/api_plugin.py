import json
import requests
from typing import Dict, Any, Optional
from loguru import logger
import allure

class APIRequest:
    def __init__(self, base_url: str = ""):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.last_response = None

    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        设置请求头
        :param headers: 请求头字典
        """
        self.session.headers.update(headers)

    @allure.step("发送API请求")
    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        发送HTTP请求
        :param method: 请求方法
        :param endpoint: 接口端点
        :param data: 表单数据
        :param json_data: JSON数据
        :param params: URL参数
        :param headers: 请求头
        :return: 响应对象
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            with allure.step(f"{method.upper()} {url}"):
                response = self.session.request(
                    method=method,
                    url=url,
                    data=data,
                    json=json_data,
                    params=params,
                    headers=headers,
                    **kwargs
                )
                
                self.last_response = response
                self._log_request_details(response)
                return response
                
        except Exception as e:
            logger.error(f"请求失败: {str(e)}")
            raise

    def _log_request_details(self, response: requests.Response) -> None:
        """
        记录请求详情
        :param response: 响应对象
        """
        with allure.step("请求详情"):
            allure.attach(
                response.request.url,
                name="Request URL",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                str(response.request.headers),
                name="Request Headers",
                attachment_type=allure.attachment_type.TEXT
            )
            if response.request.body:
                allure.attach(
                    str(response.request.body),
                    name="Request Body",
                    attachment_type=allure.attachment_type.TEXT
                )
            allure.attach(
                str(response.status_code),
                name="Response Status",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                str(response.text),
                name="Response Body",
                attachment_type=allure.attachment_type.TEXT
            )

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET请求"""
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """POST请求"""
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """PUT请求"""
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE请求"""
        return self.request("DELETE", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """PATCH请求"""
        return self.request("PATCH", endpoint, **kwargs) 