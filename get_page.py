import time

import requests
from bs4 import BeautifulSoup

def get_page(head, url, name):
    url1 = f'https://www.cbh1.cc/public/auto/search1.html?keyword={name}'

    req = requests.get(url1,headers=head)

    # 使用BeautifulSoup解析页面内容
    soup = BeautifulSoup(req.text, 'lxml')
    # bs4获取最后一页
    pages = soup.select('.myci-page')[0].select('li')[-1].select('a')[0].attrs['href']
    pages = int(pages.split('=')[-1])

    return pages
