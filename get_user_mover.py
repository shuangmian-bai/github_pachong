import time
import requests

from bs4 import BeautifulSoup

def get_user_mover(head,url_list):
    #计数器,记录当前页码
    indexs = 0
    while True:
        # 请求页
        req = requests.get(url_list[indexs], headers=head).text
        # print(url_list[indexs])

        # 新建bs4对象
        soup = BeautifulSoup(req, 'html.parser')

        # 获取这一页所存在的影视
        datas = soup.select('.stui-vodlist.clearfix')[0].select('li')

        for i in range(len(datas)):
            data = datas[i]
            cache = data.select('.stui-vodlist__thumb.lazyload')[0]
            name = cache.get('title')
            cache = [j.select('b')[0].text for j in cache.select('span')[1:]]
            # 使用 ''.join() 方法将列表中的元素拼接成一个字符串
            name = name + '__' + '__'.join(cache)
            print(f'{i} : {name}')
        if indexs != 0:
            print('w : 上一页')

        if indexs != len(url_list)-1:
            print('s : 下一页')

        cz = input('请输入您选择的操作或者需要下载的影视 : ')
        print("\033c", end="")

        #获取操作码执行操作
        if cz.upper() == 'W':
            indexs -= 1
        elif cz.upper() == 'S':
            indexs += 1
        else:
            cz = int(cz)
            root = soup.select('.col-md-6.col-sm-4.col-xs-3')[cz]
            url = root.select('.stui-vodlist__thumb.lazyload')[0].get('href')
            name = root.select('.stui-vodlist__thumb.lazyload')[0].get('title')
            return {'name':name,'url':url}