#对已完结小说页面进行爬取--不用增量式检查
#对未完结小说页面进行爬取--用增量式(借助redis数据库)检查

#

import re
import requests
import  time
import random

class ZX:
    def __init__(self):
        self.url='http://www.biquge.info/9_9890/'
        self.headers={
            'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
            'Cookie':'Hm_lvt_c979821d0eeb958aa7201d31a6991f34=1602559968,1602559972,1602559977,1602669835; Hm_lvt_6dfe3c8f195b43b8e667a2a2e5936122=1602559744,1602669858; clickbids=9890; Hm_lpvt_c979821d0eeb958aa7201d31a6991f34=1602672975; Hm_lpvt_6dfe3c8f195b43b8e667a2a2e5936122=1602669858'
        }
        self.Referer='http://www.biquge.info/9_9890/'

    def get_html(self,url):
        #发送请求，获取页面源码
        html=requests.get(url=url,headers=self.headers).content.decode()
        return html
    
    def re_func(self,html,li):
        #解析页面
        pattern=re.compile(li,re.S)
        r_list=pattern.findall(html)
        return r_list
    
    def one_html(self):
        #一级页面处理
        html=self.get_html(self.url)
        li='<dd><a href="(.*?)".*?>(.*?)</a></dd>'
        r_list=self.re_func(html,li)
        for r in r_list:
            two_url=self.url+r[0].strip()
            title=r[1]
            self.two_html(two_url,title)
            time.sleep(random.randint(2,3))
        
    def two_html(self,url,title):
        #二级页面处理
        html=self.get_html(url)
        li='<div id="content"><!--go-->(.*?)，<!--over--></div>'
        list=self.re_func(html,li)
        str_list=list[0].split('&nbsp;&nbsp;&nbsp;&nbsp;')
        print(str_list)
        # # str_list.insert(0,title)
        str='\n'.join(str_list)
        #写入文件中
        self.write_txt(str)

    def write_txt(self,str):
        #将数据写入文件里
        with open('zuxian.txt','a') as f:
            f.write(str)
    

if __name__ == "__main__":
    ZX().one_html()




