"""
    百科爬虫解析器
    1.提取inner链接,保存在list中
    2.提取内容,因为后续要做高频词汇的提取,所以我这次需要提取更多的内容,不再仅仅提取简介呢
    3.新增需要解析的内容, 词条标签, 历史编辑次数, 词条创建者,最近一次编辑时间(YYYY - MM - DD)

"""
import re
from bs4 import BeautifulSoup
from spider_module.baike.persistence_tool import BKPersistenceTool


class BKParser(object):

    def __init__(self, lemma_content, parser="html.parser"):
        self.lemma_content = lemma_content
        self.soup = BeautifulSoup(lemma_content.pop('body'), parser)

    # 经分析百度百科的词条页面发现,可能是由于百科产品迭代的原因,词条页存在两种url格式
    # 1. href = /item/%E7%AC%94%E8%AE%B0%E6%9C%AC%E7%94%B5%E8%84%91
    # 2. href = /view/1703056.htm
    # 这可能对我们的去重造成困扰,可能导致词条有两个的url,我们可能会爬了重复的页面,所以后期我们在实际存数据库的时候还是给词条的title建立唯一索引
    # 取消第二种解析格式,已经非常的少了
    # 新增,对于多义词,如果链接中含有http://baike.baidu.com/item/%E8%AF%AD%E8%A8%80?force=1,关键字force,我们不对他进行添加，因为不是我们想要的内容
    def get_inner_link(self):
        result = []
        regex1 = r"/item/.*"
        result1 = self.soup.find_all("a", href=re.compile(regex1))
        for res in result1:
            if "force" not in res['href']:
                result.append(res['href'])
        return result

    # 取得lemma_title和lemma_paras
    def get_content(self):
        # 根据css查找
        title = self.soup.find("dd", class_="lemmaWgt-lemmaTitle-title")
        if title is None:
            title = "err"
        else:
            title = title.h1.string
        paras = self.soup.find_all("div", class_="para")
        para_count = len(paras)
        content = ""
        if para_count > 80*2:
            for i in range(int(para_count/2)):
                text = paras[i].get_text()
                if text is not "" and text is not None:
                    content += text
        else:
            for j in range(para_count):
                text = paras[j].get_text()
                if text is not "" and text is not None:
                    content += text
        self.lemma_content['lemma_title'] = title
        self.lemma_content['lemma_paras'] = content
        self.lemma_content['lemma_tags'] = self.get_lemma_tags()
        self.lemma_content.update(self.get_related_info())
        return self.lemma_content

    # 取得一个词条的人工分类标签
    def get_lemma_tags(self):
        result = []
        lemma_tags = self.soup.find(id="open-tag-item")
        if lemma_tags is None:
            result.append("no categories")
        else:
            tag_items = lemma_tags.find_all("span", class_="taglist")
            for item in tag_items:
                r = item.text
                if r !="":
                    result.append(r[1:-1])
        return result

    # 返回词条相关信息
    #   - 历史编辑次数
    #   - 最后编辑时间
    #   - 词条创建者
    def get_related_info(self):
        infos = {}
        dd_description = self.soup.find("dd", class_="description")
        if dd_description is None:
            infos['history_edit_count'] = 'not catch'
            infos['last_update_time'] = 'not catch'
            infos['lemma_creator'] = 'not catch'
            return infos
        else:
            lis = dd_description.find_all("li")

        if len(lis) == 4:
            infos['history_edit_count'] = lis[1].text[5:-5]
            infos['last_update_time'] = lis[2].text[5:]
            infos['lemma_creator'] = lis[3].text[4:]
        else:
            infos['history_edit_count'] = 'not catch'
            infos['last_update_time'] = 'not catch'
            infos['lemma_creator'] = 'not catch'
        return infos

if __name__ == "__main__":
    urls = ["http://baike.baidu.com/item/c",'http://baike.baidu.com/item/%E4%BA%BA%E6%B0%91%E7%9A%84%E5%90%8D%E4%B9%89/17545218', ]
    import spider_module.baike.baike_downloader as bkd
    import spider_module.baike.common_tool as ctool
    import urllib.parse as p
    bkspyder = bkd.BKDownLoader()
    bkspyder.add_task_list(urls)
    bkspyder.download()
    r = bkspyder.get_result_list()
    # print(r[1]['body'])
    bkparser = BKParser(r[1], "lxml")
    # res1 = bkparser.get_inner_link()
    # for a in res1[:20]:
    #     # pass
    #     print(a)
    #     print(type(a))
    #     print(p.unquote(a))
    #     print(ctool.format_url("http://baike.baidu.com/item/ypl/ss", a))
    # t, c, url = bkparser.get_content()
    # print(t)
    # print(c)
    # print(url)
    # l =bkparser.get_lemma_tags()
    # l1 = bkparser.get_related_info()
    # print(l)
    # print(l1)
    lemma_content = bkparser.get_content()
    print(lemma_content['history_view_count'])
    lemma_content.pop('lemma_paras')
    for key in lemma_content.keys():
        print(key, ":", lemma_content[key],)






