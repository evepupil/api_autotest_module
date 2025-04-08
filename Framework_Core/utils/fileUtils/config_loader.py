import os
import yaml
from typing import Dict, Any, Optional
from loguru import logger

class ConfigLoader:
    def __init__(self, config_path: str = "Resources/config/config.yaml"):
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            logger.info(f"配置文件加载成功: {self.config_path}")
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            raise

    def get_value(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        :param key: 配置键，支持点号分隔的多级键
        :param default: 默认值
        :return: 配置值
        """
        try:
            value = self.config
            for k in key.split('.'):
                value = value[k]
            return value
        except (KeyError, TypeError):
            logger.warning(f"配置项不存在: {key}，使用默认值: {default}")
            return default

    def get_environment_config(self, env: str = None) -> Dict[str, Any]:
        """
        获取环境配置
        :param env: 环境名称，如果为None则使用配置文件中的默认环境
        :return: 环境配置字典
        """
        if env is None:
            env = self.get_value('default_environment', 'dev')
        
        env_config = self.get_value(f'environments.{env}', {})
        if not env_config:
            logger.warning(f"环境配置不存在: {env}，使用空配置")
        return env_config

    def update_config(self, key: str, value: Any) -> None:
        """
        更新配置值
        :param key: 配置键
        :param value: 配置值
        """
        try:
            keys = key.split('.')
            current = self.config
            for k in keys[:-1]:
                current = current.setdefault(k, {})
            current[keys[-1]] = value
            logger.info(f"配置已更新: {key} = {value}")
        except Exception as e:
            logger.error(f"更新配置失败: {str(e)}")
            raise

    def save_config(self, config_path: Optional[str] = None) -> None:
        """
        保存配置到文件
        :param config_path: 配置文件路径，如果为None则使用当前配置文件路径
        """
        try:
            save_path = config_path or self.config_path
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self.config, f, allow_unicode=True)
            logger.info(f"配置已保存到: {save_path}")
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}")
            raise

    @staticmethod
    def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并配置
        :param base_config: 基础配置
        :param override_config: 覆盖配置
        :return: 合并后的配置
        """
        result = base_config.copy()
        for key, value in override_config.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = ConfigLoader.merge_configs(result[key], value)
            else:
                result[key] = value
        return result 