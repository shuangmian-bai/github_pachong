import time

import requests
from bs4 import BeautifulSoup

def get_ji(head, url):
    # 定义返回数据字典
    datas = {}

    req = requests.get(url, headers=head)
    soup = BeautifulSoup(req.text, 'html.parser')

    # 选择集数列表
    sj = soup.select('.stui-content__playlist.clearfix')[0].select('a')
    for i in range(len(sj)):
        # 提取集数名称并去除多余空格
        ji = sj[i].text.replace('\n', '').replace(' ', '')
        # 提取集数链接
        path = sj[i].attrs['href']
        # 将集数名称和链接存入字典
        datas[path] = ji
        print(f'{i} : {ji}')

    # 获取用户输入的起始和结束序列
    while True:
        try:
            a = int(input('请输入需要下载的起始序列 : '))
            b = int(input('请输入需要下载的结束序列 : '))
            if 0 <= a <= b < len(datas):
                break
            else:
                print(f'输入的序列范围无效，请输入 0 到 {len(datas) - 1} 之间的整数。')
        except ValueError:
            print('无效输入，请输入整数。')

    # 字典键转换成列表
    keys = list(datas.keys())[a:b + 1]
    # 获取对应值
    datas = {k: datas[k] for k in keys}

    # 返回数据字典
    return datas

