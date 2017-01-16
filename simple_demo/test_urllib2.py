# -*- coding:utf-8 -*-
#测试python自带的urllib2模块的功能
import urllib2
import cookielib

url = "http://www.csdn.net"
'''
print '第一种方法:'
response_body = urllib2.urlopen(url)
print response_body.getcode()
print len(response_body.read())
'''
print '第二中方法:'
#给请求添加一个头信息
request = urllib2.Request(url)
request.add_header("User-Agent","Mozilla/5.0")
response = urllib2.urlopen(request)
print response.getcode()
#print len(response.read())
print response.read()

'''
print '第三种方法:'
#构建如需要cookie信息的请求

#创建一个cookie容器
cj = cookielib.CookieJar()
#增强urllib2.urlopen()的功能
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#安装这个opener
urllib2.install_opener(opener)
request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
response_body3 = urllib2.urlopen(request)
print response_body3.getcode()
print len(response_body3.read())
print cj
print response_body3.read()
'''

