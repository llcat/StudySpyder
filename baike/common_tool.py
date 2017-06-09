"""
    通用工具
    1.get_tag:提取某个标签中的全部文本如<header></header>信息
    2.format_url:对待添加到到数据库中的url做一些格式化处理
"""

import re
from urllib import parse


# tag可以是html中的任一标签,先截取一段在使用bs4解析应该会快些
# 使用正则表达式非贪婪匹配提取,也就是说如果有多个相同的标签
# 这个函数只会提取匹配到的第一个标签
# input: tag:str default = "html" (tag = "body","div","a"....)
# return:返回这颗标签的dom树,如果没有找到或者content本身为空,返回NoneType
def get_tag(content, tag="html"):
    if content is not None and content is not "":
        regex_str = r"<"+tag+".*?</"+tag+">"
        # caution: python中的.不匹配换行符\n,所以多行文本不加re.S标志位,它会一行一行的匹配
        match = re.search(re.compile(regex_str, re.S), content)
        if match is not None:
            return match.group()
        else:
            return None
    else:
        return None


# 转换一些进行了url编码的链接,并加上base_url
def format_url(base, url):
    new_url = parse.unquote(url)
    formatted = parse.urljoin(base, new_url)
    return formatted


def get_formatted_urls(base, urls):
    result = []
    for url in urls:
        formatted = format_url(base, url)
        result.append(formatted)
    return result


# 要取得历史浏览次数(pv)
# 需要参数newLemmaIdEnc & r(random值)来取得
# 而其中的newLemmaIdEnc是在js文件中初始化的,所以我们现在使用正则从js文件中提取
def get_newlemmaid_enc(content):
    regex = r'newLemmaIdEnc:"[a-z0-9]{24}"'
    match = re.search(re.compile(regex), content)
    if match is not None:
        result = match.group()
        result = result.split(":")
        return result[1][1:-1]
    else:
        return "null"


def get_newlemma_id(content):
    regex = r'newLemmaId:"\d+"'
    match = re.search(re.compile(regex), content)
    if match is not None:
        result = match.group()
        result = result.split(":")
        return result[1][1:-1]
    else:
        return "null"



if __name__ == "__main__":
    from spider_module.baike import baike_downloader as bkd
    down = bkd.BKDownLoader()
    down.add_task_list(['http://baike.baidu.com/item/%E5%9C%B0%E4%B8%8B%E4%B9%90%E5%9B%A2'])
    url = 'http://baike.baidu.com/item/%E5%9C%B0%E4%B8%8B%E4%B9%90%E5%9B%A2'
    raw = down.download_raw(url)
    get_newlemmaid_enc(raw)
    get_newlemma_id(raw)
