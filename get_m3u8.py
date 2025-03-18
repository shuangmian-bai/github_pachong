import re

from bs4 import BeautifulSoup
import requests
import time


def get_m3u8(head, url):
    # 忽略ssl警告
    req = requests.get(url, headers=head)

    # 使用BeautifulSoup解析页面内容
    cache = req.text

    # 使用正则表达式匹配以 http 开头并以 .m3u8 结尾的 URL
    pattern = re.compile(r'http[s]?://[^"]+\.m3u8')
    m3u8 = pattern.search(cache).group(0)

    m3u8 = m3u8.split('?url=')[-1]

    return m3u8