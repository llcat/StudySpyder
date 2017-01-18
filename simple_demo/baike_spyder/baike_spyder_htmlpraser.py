# -*- coding:utf8 -*-
# 百科爬虫HTML解析器

from bs4 import BeautifulSoup
import re
from urllib import request

class HtmlPraser(object):

    def __init__(self):
        self.contain_urls = set()
        self.target_data = {}

    def _get_all_link(self,soup):
        a_tags = soup.find_all('a',href = re.compile(r'/view/\d+\.htm'))
        #print(a_tags)
        for a_tag in a_tags:
            href = a_tag['href']
            url = "http://baike.baidu.com"+href
            #print(url)
            self.contain_urls.add(url)
        return self.contain_urls
    
    
##    简介：
##    <div class="lemma-summary" label-module="lemmaSummary">
##    <div class="para" label-module="para">
##    GPL，是General Public License的缩写，
##    是一份GNU通用公共授权非正式的中文翻译。
##    它并非由自由软件基金会所发表，亦非使用GNU通用公共授权
##    的软件的法定发布条款─直有GNU通用公共授权英文原文的版本始具有此等效力。
##    </div>
##    </div>
##    标题：
##    <dd class="lemmaWgt-lemmaTitle-title">
##    <h1>GPL</h1>
##    </dd>
  

    def _get_target_data(self,soup):
        title = soup.find(class_ ='lemmaWgt-lemmaTitle-title').find('h1').string
        #print(title)
        #print(type(title))
        self.target_data['title'] = title
        summary = soup.find(class_ ='lemma-summary').find(class_='para').getText()
        #print(summary)
        self.target_data['summary'] = summary
        return self.target_data
        
    def prase(self,html_content):
        if html_content is None:
            return
        soup = BeautifulSoup(html_content,'html.parser',from_encoding='utf-8')
        #print(html_content)
        #获取所有符合要求的a标签
        self.contain_urls= self._get_all_link(soup)
        self.target_data = self._get_target_data(soup)
        return self.contain_urls,self.target_data


##response = request.urlopen('http://baike.baidu.com/view/309208.htm')
##html = response.read()
##praser = HtmlPraser()
##praser.prase(html)

