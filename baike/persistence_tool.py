"""
    @author: plyu
    百科爬虫持久化工具(使用mongoDB数据库)
    1.保存待爬取url
    2.查找已爬取url
    3.保存词条页的标题和内容
"""
import pymongo
from pymongo import MongoClient as mongoc


# 存在数据库spider_module_data
# 在mongo中,不同的表是collection,每条数据是document,并且collection是没有归定schema的,所以document是可伸缩的,但是我们最好还是存储格式一致的数据
class BKPersistenceTool(object):

    # 默认主机:127.0.0.1, port = 27017
    def __init__(self):
        try:
            self.client = mongoc()
            self.db = self.client['spider_module_data']
            self.coll_new_url = self.db['new_urls']
            self.coll_old_url = self.db['old_urls']
            self.coll_content = self.db['lemma_contents']
            self.coll_new_url.create_index([("new_url", pymongo.ASCENDING)], unique=True)
            self.coll_old_url.create_index([("old_url", pymongo.ASCENDING)], unique=True)
            self.coll_content.create_index([("lemma_id", pymongo.ASCENDING)], unique=True)
        except Exception as e:
            print(e.args)

    # 添加一组新的url到数据库中
    def add_new_urls(self, urls):
        filtered_urls = []
        if urls is not None:
            for url in set(urls):
                if self.is_crawled(url):
                    pass
                    # print("%s is crawled" % url)
                else:
                    filtered_urls.append(url)
        for f_url in filtered_urls:
            try:
                self.coll_new_url.insert_one({"new_url": f_url})
            except Exception as e:
                print("in add_new_url:", e.args)
                continue

    # 判断一个url是否被爬取过,或者已经存在
    def is_crawled(self, url):
        query_1 = {"old_url": url}
        if self.coll_old_url.find(query_1).count() > 0:
            return True
        else:
            query_2 = {"new_url": url}
            if self.coll_new_url.find(query_2).count() > 0:
                return True
            else:
                return False

    # 取得一个待爬取的任务列表
    # length:指定任务列表长度
    # return:返回任务列表
    def get_task_list(self, length):
        count = self.coll_new_url.count()
        task_list = []
        if count == 0:
            return task_list
        if length > count:
            length = count
        get_list = self.coll_new_url.find({}, limit=length)
        for task in get_list:
            try:
                task_list.append(task['new_url'])
                self.add_old_url(task['new_url'])
                self.coll_new_url.delete_one(task)
            except Exception as e:
                print("in get_task_list: ", e.args)
                continue
        return task_list

    # content:词条,词条内容,url
    # return:正常添加返回True,否则抛出异常,返回False
    def add_content(self, content):
        try:
            self.coll_content.insert_one(content)
        except Exception as e:
            print("in add_content", "lemma_id: ", content['lemma_id'], "\n", "url: ", content['lemma_url'], "\n", e.args)
            return False
        return True

    def add_old_url(self, url):
        try:
            self.coll_old_url.insert_one({'old_url': url})
        except Exception as e:
            print("in add_old_urls: ", e.args)

    # 先前抓取过得url需要重新抓取，将old_urls中的数据转移到new_urls中
    def mv_old_new(self):
        count = self.coll_old_url.count()
        for i in range(count):
            f_dr = self.coll_old_url.find_one_and_delete({})
            self.coll_new_url.insert_one({'new_url': f_dr['old_url']})

if __name__ == "__main__":
    bkp = BKPersistenceTool()
    urls_test = ["www.11.com",
                 "www.22.com",
                 "www.11.com",
                 "www.33.com",
                 "www.44.com"]
    # bkp.add_new_urls(urls_test)
    # r1 = bkp.get_task_list(3)
    # for i in r1:
    #     print(i)
    # print(bkp.coll_new_url.count({}))
    content_list_test = [
        {
            "title": "Pyy",
            "content": "sssssssssssdada汗大大打算大外都会以和",
            "url": "www.sda.com"
        },
        {
            "title": "Gom",
            "content": "Python[1]  （英国发音：/ˈpaɪθən/ 美国发音：/ˈpaɪθɑːn/）",
            "url": "www.sda.com"
        },
        {
            "title": "Pyyy",
            "content": "sssssssssssdada汗大大打算大外都会以和",
            "url": "www.sda.com"
        },
        {
            "title": "err",
            "content": "",
            "url": "www.sda.com"
        }
    ]
    # for content_test in content_list_test:
    #     bkp.add_content(content_test)
    # r2 = bkp.get_task_list(4)
    # test_db = bkp.client['test']
    # test_coll = test_db['name']
    # data = {"name": "llcat1"}
    # # test_coll.create_index([("_name", pymongo.HASHED)])
    # # test_coll.drop_index([("_name", pymongo.HASHED)])
    # print(test_coll.index_information())
    # test_coll.insert_one(data)
    # print(test_coll.find({"name": "llcat"}))
    # print(test_coll.count())
    # print(bkp.coll_content.index_information())
    # result = test_coll.find({}, limit=3)
    # for r in result:
    #     test_coll.delete_one(r)
    bkp.mv_old_new()