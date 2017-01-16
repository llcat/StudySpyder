# coding:utf8 -*-
# 百科爬虫 url管理器

class UrlManager(object):
    
    def __init__(self):
        self.old_urlset = set()
        self.new_urlset = set()

    def add_new_url(self,new_url):
        if new_url is not in old_urlset:
            new_urlset.add(new_url)
  
    def add_new_urls(self,new_urls):
        for url in new_urls:
            add_new_url(url)

    def has_new_url():
        return len(new_urlset) != 0

    def get_new_url():
        new_url = new_urlset.pop()
        old_urlset.add(new_url)


