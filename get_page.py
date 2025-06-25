import time
import logging

import requests
from bs4 import BeautifulSoup

def get_page(head, url, name):
    try:
        req = requests.get(url, headers=head)
        req.raise_for_status()
    except requests.RequestException as e:
        logging.error(f'获取页面时发生错误: {e}')
        return 1

    # 使用BeautifulSoup解析页面内容
    soup = BeautifulSoup(req.text, 'html.parser')
    # bs4获取最后一页
    pages = soup.select('.stui-page__item.text-center.clearfix')[0].select('li')[-1].select('a')[0].get('href')
    pages = pages.split('page/')[1]
    pages = pages.split('/')[0]
    pages = int(pages)

    return pages
