import time
import requests

from bs4 import BeautifulSoup

def get_user_mover(head,url_list):
    #计数器,记录当前页码
    indexs = 0

    while True:
        # 请求页
        req = requests.get(url_list[indexs], headers=head).text
        print(url_list[indexs])

        # 新建bs4对象
        soup = BeautifulSoup(req, 'lxml')

        # 获取这一页所存在的影视
        datas = soup.select('.myci-vodlist__media')[0].select('li')

        for i in range(len(datas)):
            data = datas[i]
            name = data.select('.detail')[0].select('a')[0].text
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
            root = soup.select('.myci-vodlist__media')[0].select('li')[int(cz)].select('.detail')[0].select('a')[0]
            url = root.attrs['href']
            name = soup.select('.myci-vodlist__media')[0].select('li')[int(cz)].select('.detail')[0].select('a')[0].text
            return {'name':name,'url':url}