import re
import logging

from bs4 import BeautifulSoup
import requests
import time


def get_m3u8(head, url):
    # 忽略ssl警告
    try:
        req = requests.get(url, headers=head)
        req.raise_for_status()
    except requests.RequestException as e:
        logging.error(f'获取 m3u8 时发生错误: {e}')
        return None

    # 使用BeautifulSoup解析页面内容
    try:
        cache = req.text
        soup = BeautifulSoup(cache, 'html.parser')
        m3u8 = soup.select('.stui-player__video.embed-responsive.embed-responsive-16by9.clearfix')[0].select('script')[0].text
        m3u8 = m3u8.split(',"url":')[1]
        m3u8 = m3u8.split('"')[1]
        m3u8 = m3u8.replace(r'\/', '/')
        m3u8 = m3u8.encode('utf-8').decode('unicode_escape')
    except Exception as e:
        logging.error(f'解析页面内容时发生错误: {e}')
        return None

    try:
        req = requests.get(m3u8, headers=head)
        req.raise_for_status()
    except requests.RequestException as e:
        logging.error(f'获取 m3u8 文件时发生错误: {e}')
        return None

    try:
        datas = req.text.split('\n')
        if len(datas) < 5:
            cache = [i for i, x in enumerate(datas) if x.find('.m3u8') != -1][0]
            cache = datas[cache]

            if cache[0:4] == 'http':
                m3u8 = cache
            else:
                m3u8 = m3u8[:m3u8.rfind('/')+1]+cache
    except Exception as e:
        logging.error(f'处理 m3u8 数据时发生错误: {e}')
        return None

    return m3u8

