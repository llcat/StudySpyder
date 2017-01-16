# -*- coding:utf8 -*-
# 百科爬虫HTML解析器

from bs4 import BeautifulSoup
import re
from urllib import request
class HtmlPraser(object):

    def __init__(self):
        self.contain_urls = set()
        self.target_data = None

    def _get_all_link(soup):
        a_tags = soup.find_all('a',href = re.compile(r'/view/\d+/.htm'))
        for a_tag in a_tags:
            href = a_tag['href']
            url = "http://baike.baidu.com"+href
            contain_urls.add(url)
        return contain_urls

    def _get_target_data(soup):
        
    def prase(self,html_content):
        if html_content is None:
            return
        soup = BeautifulSoup(html_content,'html.parser',from_encoding='utf-8')
        #print(html_content)
        #获取所有符合要求的a标签
        contain_urls = _get_all_link(soup)
        target_data = _get_target_data(soup)
        return contain_urls,target_data


#response = request.urlopen('http://baike.baidu.com/view/21087.htm')
#html = response.read()
#praser = HtmlPraser()
#praser.prase(html)

