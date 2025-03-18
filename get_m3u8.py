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
    print(m3u8)

    req = requests.get(m3u8,headers=head)

    datas = req.text.split('\n')
    if len(datas) < 5:
        cache = [i for i, x in enumerate(datas) if x.find('.m3u8') != -1][0]
        cache = datas[cache]

        if cache[0:4] == 'http':
            m3u8 = cache
        else:
            m3u8 = m3u8[:m3u8.rfind('/')+1]+cache

    return m3u8