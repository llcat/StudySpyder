# -*- coding:utf8 -*-
# 百科爬虫HTML下载器
from urllib import request

class HtmlDownLoader(object):

    def __init__(self):
        pass

    def download(self,url):
        response = request.urlopen(url)
        if response.getcode() == 200:
            html_content = response.read()
            #print(html_content)
            return html_content
        else:
            return None


##obj = HtmlDownLoader()
##obj.download("http://baike.baidu.com/view/21087.htm")
