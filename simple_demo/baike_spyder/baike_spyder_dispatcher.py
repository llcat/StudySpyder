# -*- coding:utf8 -*-
#百科爬虫调度器
import baike_spyder_urlmanager
import baike_spyder_htmldownloader
import baike_spyder_htmlpraser
import baike_spyder_outputer
class Dispatcher(object):

    #初始化需要的模块
    def __init__(self):
        self.urlmanager = baike_spyder_urlmanager.UrlManager()
        self.htmldownloader = baike_spyder_htmldownloader.HtmlDownLoader()
        self.htmlpraser = baike_spyder_htmlpraser.HtmlPraser()
        self.outputer = baike_spyder_outputer.HtmlOutputer()

    #抓取操作
    def craw(self,enter_url):
        count = 1
        self.urlmanager.add_new_url(enter_url)
        while self.urlmanager.has_new_url():
            try:
                if count == 50:
                    break
                current_url = self.urlmanager.get_new_url()
                #print(current_url)
                print("第%d条,url = %s"%(count,current_url))
                count = count+1
                html_content = self.htmldownloader.download(current_url)
                #print(html_content)
                contain_urls,target_data = self.htmlpraser.prase(html_content)
                self.urlmanager.add_new_urls(contain_urls)
                self.outputer.collect_data(target_data)
                #print(self.outputer.get_collected_data())
            except:
                print("craw %d failed"%count)
        #print(self.outputer.get_collected_data())
        #self.outputer.output_html()
        self.outputer.output2mongo()
     
if __name__ == "__main__":
    enter_url = "http://baike.baidu.com/view/3105539.htm"
    dispatcher = Dispatcher()
    dispatcher.craw(enter_url)
