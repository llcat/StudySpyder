# -*- coding:utf8 -*-
#输出器，输出爬取的数据到html文件中
class HtmlOutputer(object):

    def __init__(self):
        self.collected_data = []

    def collect_data(self,target_data):
        data = {}
        data['title'] = target_data['title']
        data['summary'] = target_data['summary']
        if target_data is not None:
            self.collected_data.append(data)

    def get_collected_data(self):
        return self.collected_data

    def output_html(self):
        html_file = open('collect_data.html','w')
        html_file.write("<html>")
        html_file.write("<body>")
        html_file.write('<table style="border:1px solid black;backgroud:green">')
        for data in self.collected_data :
            title = data['title']
            summary = data['summary']
            td1 = "<td>"+title+"</td>"
            td2 = "<td>"+summary+"</td>"
            html_file.write('<tr style="border:1px solid black>')
            td2=td2.replace(u'\xa0', u' ') 
            html_file.write(td1)
            html_file.write(td2)
            html_file.write('</tr>')
        html_file.write("</table>")
        html_file.write("</body>")
        html_file.write("</html>")
            
