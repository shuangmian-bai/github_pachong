import os
import requests
from bs4 import BeautifulSoup
from print_banner import print_banner

def validate_input(prompt, cast_type=str):
    while True:
        try:
            value = cast_type(input(prompt))
            return value
        except ValueError:
            print('无效输入，请输入正确的值。')

def clear_console():
    print_banner()

def parse_episodes(soup):
    """解析集数信息"""
    datas = {}
    sj = soup.select('.stui-content__playlist.clearfix')[0].select('a')
    for i in range(len(sj)):
        ji = sj[i].text.replace('\n', '').replace(' ', '')
        path = sj[i].attrs['href']
        datas[path] = ji
        print(f'{i} : {ji}')
    return datas

def get_ji(head, url):
    clear_console()
    req = requests.get(url, headers=head)
    soup = BeautifulSoup(req.text, 'html.parser')
    datas = parse_episodes(soup)
    while True:
        a = validate_input('请输入需要下载的起始序列 : ', cast_type=int)
        b = validate_input('请输入需要下载的结束序列 : ', cast_type=int)
        if 0 <= a <= b < len(datas):
            break
        else:
            print(f'输入的序列范围无效，请输入 0 到 {len(datas) - 1} 之间的整数。')
    keys = list(datas.keys())[a:b + 1]
    datas = {k: datas[k] for k in keys}
    return datas
