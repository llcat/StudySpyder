# -*- coding:utf8 -*-
#百科爬虫调度器
from baike_spyder import *
class Dispatcher(object):

    #初始化需要的模块
    def __init__(self):
        self.urlmanager = baike_spyder_urlmanager.UrlManager()
        self.htmldownloader = baike_spyder_htmldownloader.HtmlDownLoader()
        self.htmlpraser = baike_spyder_htmlpraser.HtmlPraser()
        self.outputer = baike_spyder_outputer.Outputer()

    #抓取操作
    def craw(self,enter_url):
        count = 1
        urlmanager.add_new_url(enter_url)
        while urlmanager.has_new_url():
            try:
                current_url = urlmanager.get_new_url()
                print("第%d条,url = %s"%(count,current_url))
                html_content = htmldownloader.download(current_url)
                contain_urls,target_data = htmlpraser.prase(html_content)
                urlmanager.add_new_urls(contain_urls)
                outputer.collect_data(target_data)
                if count == 1000:
                    break
            except:
                print("craw %d failed"%count)
            finally:
                count = count+1       
        outputer.output_html()
     
if __name__ == "__main__":
    enter_url = "http://baike.baidu.com/view/21087.htm"
    dispatcher = Dispatcher()
    dispatcher.craw()
