# coding:utf8 -*-
# 百科爬虫 url管理器
#目前的url是采用的最简单的管理方式,只保证了单次爬取过程的去重
#下一步应该确保对于已经采集过得页面，在下次启动爬虫时不再对他采集，所以应该持久化数据
#更改url的存放位置为mongo

class UrlManager(object):
    
    def __init__(self,spyder_dao):
        self.old_url_coll = spyder_dao.workCollection("baikespyder", "old_urls")
        self.new_url_coll = spyder_dao.workCollection("baikespyder", "new_urls")

    def add_new_url(self,new_url):
        url = {"new_url":new_url}
        if self.isCrawed(url):
            pass
        else:
            if self.new_url_coll.find({"new_url": url['new_url']}).count()==0:
                self.new_url_coll.insert_one(url)

                  
    def add_new_urls(self,new_urls):
        for url in new_urls:
            self.add_new_url(url)
        
    def has_new_url(self):
        return self.new_url_coll.find().count() != 0

    def get_new_url(self):
        cursor = self.new_url_coll.find()
        new_url = cursor[0]
        #print(new_url)
        add_url = {"old_url":new_url["new_url"]}
        if self.old_url_coll.find({"old_url":add_url['old_url']}).count() == 0:
            self.old_url_coll.insert_one(add_url)
        else:
            pass
        result = self.new_url_coll.delete_one({"new_url":new_url['new_url']})
        return new_url["new_url"]

    def isCrawed(self,url):
        cursor = self.old_url_coll.find({"new_url":url["new_url"]})
        if cursor.count() == 0:
            return False
        else:
            return True


