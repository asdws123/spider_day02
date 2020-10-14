import pymongo
# #1.创建链接对象
# connect=pymongo.MongoClient(host='localhost',port=27017)
# #2.创建库对象
# db=connect['guazidb']
# #3.创建集合对象
# set=db['guaziset']
# #4.插入数据
# set.insert_one({'name':'K/DA','age':18})
"""
一级页面:
    详情页链接
二级页面:
    1、汽车名称
    2、行驶里程
    3、排量
    4、变速箱
    5、价格
"""
import requests
import re
import time
import random
import csv
import redis
from hashlib import md5

class GuaziSpider:
    def __init__(self):
        """定义常用变量"""
        self.url = 'https://www.guazi.com/bj/buy/o{}/#bread'
        self.headers = {
            'Cookie':'antipas=263DD622X821930537h3545339V; uuid=0e9199bc-070b-4fc7-9bcd-48a2f6734b52; cityDomain=www; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22self%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%220e9199bc-070b-4fc7-9bcd-48a2f6734b52%22%2C%22ca_city%22%3A%22hz%22%2C%22sessionid%22%3A%227e293493-a603-496f-91a9-e6fa6cf41018%22%7D; user_city_id=-1; preTime=%7B%22last%22%3A1602574057%2C%22this%22%3A1602558281%2C%22pre%22%3A1602558281%7D; ganji_uuid=5283289900892170456860; lg=1',
            'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'
        }

        #1.创建mongo链接对象
        self.connect=pymongo.MongoClient(host='localhost',port=27017)
        #2.创建库对象
        self.db=self.connect['guazidb']
        #3.创建集合对象
        self.set=self.db['guaziset']

        # 连接redis数据库
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def get_html(self, url):
        """功能函数1: 发请求获取响应内容"""
        html = requests.get(url=url, headers=self.headers).content.decode('utf-8')

        return html

    def md5_url(self,url):
        """功能函数3：对url进行md5加密"""
        s=md5()
        s.update(url.encode())
        s=s.hexdigest()
        return s

    def re_func(self, regex, html):
        """功能函数2: 正则解析获取列表"""
        pattern = re.compile(regex, re.S)
        r_list = pattern.findall(html)

        return r_list

    def parse_html(self, one_url):
        """爬虫逻辑函数 - 从一级页面开始抓取"""
        one_html = self.get_html(url=one_url)
        one_regex = '<li data-scroll-track=.*?href="(.*?)"'
        # href_list: ['/su/xxx', '/su/xxx', '', ..., '']
        href_list = self.re_func(one_regex, one_html)
        for href in href_list:
            two_url = 'https://www.guazi.com' + href
            finger = self.md5_url(url=two_url)
            # 返回值1:说明之前没抓过
            if self.r.sadd('guazi:spider', finger) == 1:
                # 获取一辆汽车详情页数据的函数
                self.get_one_car_info(two_url)
                # 控制频率
                time.sleep(random.randint(2, 3))

    def get_one_car_info(self, two_url):
        """获取一辆汽车的具体数据"""
        two_html = self.get_html(url=two_url)
        two_regex = '<div class="product-textbox">.*?<h2 class="titlebox">(.*?)</h2>.*?<li class="two"><span>(.*?)</span>.*?<li class="three"><span>(.*?)</span>.*?<li class="last"><span>(.*?)</span>.*?<span class="price-num">(.*?)</span>'
        # car_info_list: [('','','','','')]
        car_info_list = self.re_func(two_regex, two_html)
        item = {}
        item['name'] = car_info_list[0][0].strip().split('\r\n')[0]
        item['km'] = car_info_list[0][1].strip()
        item['displace'] = car_info_list[0][2].strip()
        item['type'] = car_info_list[0][3].strip()
        item['price'] = car_info_list[0][4].strip()
        print(item)

        #往mongo数据库插入数据
        self.set.insert_one(item)

    def run(self):
        for o in range(1, 2):
            page_url = self.url.format(o)
            self.parse_html(one_url=page_url)

if __name__ == '__main__':
    spider = GuaziSpider()
    spider.run()











































