# coding:utf8 -*-
# 百科爬虫 url管理器

class UrlManager(object):
    
    def __init__(self):
        self.old_urlset = set()
        self.new_urlset = set()

    def add_new_url(self,new_url):
        #print(new_url)
        if new_url not in self.old_urlset:
            self.new_urlset.add(new_url)
                  
    def add_new_urls(self,new_urls):
        for url in new_urls:
            self.add_new_url(url)
        #print(self.new_urlset)
        
    def has_new_url(self):
        return len(self.new_urlset) != 0

    def get_new_url(self):
        new_url = self.new_urlset.pop()
        self.old_urlset.add(new_url)
        return new_url


