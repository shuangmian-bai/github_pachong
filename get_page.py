import time
import logging

import requests
from bs4 import BeautifulSoup

def fetch_page(head, url):
    try:
        req = requests.get(url, headers=head)
        req.raise_for_status()
        return req.text
    except requests.RequestException as e:
        logging.error(f'获取页面时发生错误: {e}')
        return None

def parse_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.select('.stui-page__item.text-center.clearfix')[0].select('li')[-1].select('a')[0].get('href')
    pages = pages.split('page/')[1]
    pages = pages.split('/')[0]
    return int(pages)

def get_page(head, url, name):
    html = fetch_page(head, url)
    if not html:
        return 1
    return parse_total_pages(html)
