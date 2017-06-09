"""
    @author: pl_yu
    百科爬虫调度器
    调用其他模块,处理全部的业务逻辑
    整理下思路:
    1.结束条件是完成需要爬取的url条数,在start()中给定
    2.主进程和3个downloader间需要通信
      如下载任务完成需要通知url manager进程分派新的url,
      下载完成后的url和内容应该是存放在共享的list的中,3个downloader争用情况下应该加锁

"""

from spider_module.baike.baike_downloader import BKDownLoader
from spider_module.baike.baike_parser import BKParser
from spider_module.baike.persistence_tool import BKPersistenceTool
from spider_module.baike.baike_urlmanager import BKUrlManager
from spider_module.baike.common_tool import *
from multiprocessing import Manager, Process, Queue, Lock
import os
import time
import random

class BKDispatcher(object):

    def __init__(self):
        self.completed_list = Manager().list()
        self.p_tool = BKPersistenceTool()

    def parser(self, lemma_content):
        parser = BKParser(lemma_content, "lxml")
        data = parser.get_content()
        self.p_tool.add_content(data)
        urls = parser.get_inner_link()
        formatted = get_formatted_urls(lemma_content['lemma_url'], urls)
        self.p_tool.add_new_urls(formatted)

    # url生产者进程
    @staticmethod
    def url_manager(message_ques, counter, tasks):
        print("url manager-%d is starting..." % (os.getpid()))
        downloader_count = 3
        url_manager = BKUrlManager()
        per_num = 5
        for mess_que in message_ques:
            mess_que['receive_q'].put(url_manager.get_tasks(1))
        while True:
            if downloader_count == 0:
                print("url manager completed task ...")
                break
            for mess_que in message_ques:
                try:
                    # 每个downloader会在完成任务后重新请求新的url
                    flag = mess_que['send_q'].get(block=False)
                    if "done" == flag:
                        downloader_count -= 1
                    if flag is True:
                        # manager在这里判断是否还需要派发新的任务
                        # 如果counter >= tasks,不再派发新的url,发送finish消息
                        if counter.value >= tasks:
                            mess_que['receive_q'].put("finish")
                        else:
                            # ToDo:某种情况下,db中的url库存不足时,应该做处理
                            task_urls = url_manager.get_tasks(per_num)
                            counter.value += len(task_urls)
                            mess_que['receive_q'].put(task_urls)
                    elif flag is False:
                        print("warning....check url stock")
                        task_urls = url_manager.get_tasks(per_num)
                        counter.value += per_num
                        mess_que['receive_q'].put(task_urls)
                except Exception as e:
                    continue

    # url消费者进程(3个),与生产者间使用Queue通信,与主进程共享变量completed_list
    @staticmethod
    def downloader(d_q, completed_l, lock):
        print("downloader-%d is starting..." % (os.getpid()))
        downloader = BKDownLoader()
        while True:
            mess_obj = d_q['receive_q'].get()
            if "finish" == mess_obj:
                print("downloader-%d is finished" % (os.getpid()))
                d_q['send_q'].put("done")
                break
            else:
                if len(mess_obj) > 0:
                    time.sleep(random.randint(1, 3))
                    downloader.add_task_list(mess_obj)
                    downloader.download()
                    results = downloader.get_result_list()
                    with lock:
                        for r in results:
                            completed_l.append(r)
                    d_q['send_q'].put(True)
                    print("the downloader-%d complete some task" % (os.getpid()))
                else:
                    d_q['send_q'].put(False)
                    print("the downloader-%d may not work,check url stock!" % (os.getpid()))

    # 开始任务
    def start(self, task_num):
            def prepare_url():
                if self.p_tool.coll_new_url.find({}).count() == 0:
                    start = ["http://baike.baidu.com/item/Python", ]
                    bkd = BKDownLoader()
                    bkd.add_task_list(start)
                    bkd.download()
                    r = bkd.get_result_list()
                    self.parser(d_url=r[0]['url'], content=r[0]['body'])
                else:
                    pass
            prepare_url()
            # 进程间通信队列
            d_queues = [{"send_q": Queue(), "receive_q": Queue()}]*3
            # 控制变量,url分发计数器
            count = Manager().Value("i", 0)
            # 访问completed_list加锁
            list_lock = Lock()
            # url manager进程开启
            process_manager = Process(target=self.url_manager, args=(d_queues, count, task_num))
            process_manager.start()
            # downloader进程开启
            downloader_list = []
            for d_que in d_queues:
                p = Process(target=self.downloader, args=(d_que, self.completed_list, list_lock))
                downloader_list.append(p)
                p.start()
            # 主进程的退出条件?
            # 其他4个进程全部结束
            while True:
                if len(self.completed_list) > 0:
                    content = self.completed_list.pop()
                    self.parser(content)
                if len(self.completed_list) == 0:
                    # 首先检查manager是否还在运行
                    # 如果还在运行,直接continue
                    if process_manager.is_alive():
                        continue
                    else:
                        exit_flag = False
                        for p in downloader_list:
                            exit_flag = exit_flag or p.is_alive()
                        if exit_flag is False:
                            print("main process completed.....")
                            break
                        else:
                            continue


if __name__ == "__main__":
    dispatcher = BKDispatcher()
    dispatcher.start(50000)


