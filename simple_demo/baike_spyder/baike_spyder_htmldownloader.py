# -*- coding:utf8 -*-
# 百科爬虫HTML下载器
from urllib import request

class HtmlDownLoader(object):

    def __init__(self):
        pass

    def download(self,url):
        response = request.urlopen()
        if response.getcode() == 200:
            return response.read()
        else:
            return None
