import time
from typing import List, Dict, Any, Callable
from datetime import datetime
from loguru import logger
import threading

class TestScheduler:
    def __init__(self):
        self.tasks = []
        self._running = False
        self._scheduler_thread = None

    def add_task(self, task: Dict[str, Any]) -> None:
        """
        添加测试任务
        :param task: 任务配置字典
        """
        self.tasks.append(task)
        logger.info(f"已添加任务: {task.get('name', 'unnamed task')}")

    def remove_task(self, task_id: str) -> bool:
        """
        移除测试任务
        :param task_id: 任务ID
        :return: 是否成功移除
        """
        for task in self.tasks:
            if task.get('id') == task_id:
                self.tasks.remove(task)
                logger.info(f"已移除任务: {task_id}")
                return True
        return False

    def start(self) -> None:
        """启动调度器"""
        if self._running:
            logger.warning("调度器已在运行中")
            return

        self._running = True
        self._scheduler_thread = threading.Thread(target=self._run_scheduler)
        self._scheduler_thread.start()
        logger.info("调度器已启动")

    def stop(self) -> None:
        """停止调度器"""
        self._running = False
        if self._scheduler_thread:
            self._scheduler_thread.join()
        logger.info("调度器已停止")

    def _run_scheduler(self) -> None:
        """调度器主循环"""
        while self._running:
            current_time = datetime.now()
            
            for task in self.tasks:
                if self._should_run_task(task, current_time):
                    self._execute_task(task)
            
            time.sleep(1)  # 避免过度消耗CPU

    @staticmethod
    def _should_run_task(task: Dict[str, Any], current_time: datetime) -> bool:
        """
        检查任务是否应该执行
        :param task: 任务配置
        :param current_time: 当前时间
        :return: 是否应该执行
        """
        schedule_time = task.get('schedule_time')
        if not schedule_time:
            return False
        
        # 这里可以实现更复杂的调度逻辑
        return True

    def _execute_task(self, task: Dict[str, Any]) -> None:
        """
        执行测试任务
        :param task: 任务配置
        """
        try:
            if callable(task.get('callback')):
                task['callback'](task)
            logger.info(f"任务执行完成: {task.get('name', 'unnamed task')}")
        except Exception as e:
            logger.error(f"任务执行失败: {str(e)}")

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        获取任务状态
        :param task_id: 任务ID
        :return: 任务状态信息
        """
        for task in self.tasks:
            if task.get('id') == task_id:
                return {
                    'id': task_id,
                    'name': task.get('name'),
                    'status': task.get('status', 'unknown'),
                    'last_run': task.get('last_run'),
                    'next_run': task.get('next_run')
                }
        return {} 