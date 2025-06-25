import re
import logging

from bs4 import BeautifulSoup
import requests
import time


def get_m3u8(head, url):
    """获取 m3u8 文件地址"""
    try:
        req = requests.get(url, headers=head)
        req.raise_for_status()
        soup = BeautifulSoup(req.text, 'html.parser')
        script_text = soup.select_one('.stui-player__video script').text
        m3u8 = re.search(r'"url":"(.*?)"', script_text).group(1).replace(r'\/', '/')
        m3u8 = m3u8.encode('utf-8').decode('unicode_escape')
    except (requests.RequestException, AttributeError, IndexError) as e:
        logging.error(f'获取或解析 m3u8 时发生错误: {e}')
        return None

    try:
        req = requests.get(m3u8, headers=head)
        req.raise_for_status()
        datas = req.text.split('\n')
        if len(datas) < 5:
            sub_m3u8 = next((line for line in datas if '.m3u8' in line), None)
            if sub_m3u8:
                m3u8 = sub_m3u8 if sub_m3u8.startswith('http') else f"{m3u8.rsplit('/', 1)[0]}/{sub_m3u8}"
    except requests.RequestException as e:
        logging.error(f'获取子 m3u8 文件时发生错误: {e}')
        return None

    return m3u8

