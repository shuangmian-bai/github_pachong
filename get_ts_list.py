import time
import logging

import requests
from bs4 import BeautifulSoup

def get_ts_list(head, m3u8):
    try:
        rel = requests.get(m3u8, headers=head)
        rel.raise_for_status()
    except requests.RequestException as e:
        logging.error(f'获取 ts 列表时发生错误: {e}')
        return []

    # 初始化返回列表
    ts_list = []

    logging.info(f'状态码为 : {rel.status_code}')

    if rel.status_code == 200:
        # 看看有没有子地址
        datas = rel.text.split('\n')
        m3u8 = m3u8[:m3u8.rfind('/') + 1]
        if len(datas) < 5:
            cache = [i for i, x in enumerate(datas) if x.find('.m3u8') != -1][0]
            cache = datas[cache]
            if cache[0:4] == 'http':
                m3u8 = cache
            else:
                m3u8 = m3u8 + cache

            logging.info('发现子m3u8等待10s后继续')
            logging.info(f'm3u8地址为 : {m3u8}')
            time.sleep(10)
            ts_list = get_ts_list(head, m3u8)
            return ts_list
        else:
            # 定义可能的后缀列表
            valid_extensions = ['.ts', '.mp4', '.m4s', '.jpeg']  # 根据实际情况添加或修改后缀
            a = 0
            for data in datas:
                if any(data.endswith(ext) for ext in valid_extensions):
                    if a == 0:
                        lens = len(data)
                        a += 1
                    if len(data) != lens:
                        continue
                    if data[0:4] == 'http':
                        ts = data
                    else:
                        ts = m3u8 + data
                    ts_list.append(ts)

            return ts_list

    # 如果错误直接返回空ts
    else:
        logging.error(f'请求失败，状态码为: {rel.status_code}')
        return []
