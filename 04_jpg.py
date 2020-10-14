import requests
import os
#抓取图片
url='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1602665746997&di=661cc4382b3ea2346928ab7391611e54&imgtype=0&src=http%3A%2F%2Fn.sinaimg.cn%2Ffront%2F530%2Fw852h478%2F20181128%2F5GmR-hpinrya6826424.jpg'
headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'}
#1.获取bytes数据类型
html=requests.get(url=url,headers=headers).content

#2.创建文件保存目录
dir='./images/LOL_KDA/'
if not os.path.exists(dir):
    os.makedirs(dir)

#3.将图片保存到本地文件中
#图片命名:./images/LOL_KDA/xxx.jpg
filename=dir+url[-16:]
with open(filename,'wb') as f:
    f.write(html)
