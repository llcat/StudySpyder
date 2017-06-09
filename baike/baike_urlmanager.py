"""
    bai_ke url管理器:
    1.分发 task url到下载器
    2.存储待爬url到db
    3. url管理器在这并没有做什么其他的工作，如果后续有需要，爬取策略应该在这里实现
"""

from spider_module.baike import common_tool as ctool
from spider_module.baike import persistence_tool as ptool


class BKUrlManager(object):

    def __init__(self):
        self.p_tool = ptool.BKPersistenceTool()

    def get_tasks(self, num):
        return self.p_tool.get_task_list(num)
