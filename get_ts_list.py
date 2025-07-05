import time
import logging
import requests

def fetch_m3u8(head, m3u8):
    try:
        rel = requests.get(m3u8, headers=head)
        rel.raise_for_status()
        return rel
    except requests.RequestException as e:
        logging.error(f'获取 ts 列表时发生错误: {e}')
        return None

def parse_ts_list(m3u8_url, text):
    ts_list = []
    datas = text.split('\n')
    m3u8_base = m3u8_url[:m3u8_url.rfind('/') + 1]
    valid_extensions = ['.ts', '.mp4', '.m4s', '.jpeg']
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
                ts = m3u8_base + data
            ts_list.append(ts)
    return ts_list

def get_ts_list(head, m3u8):
    rel = fetch_m3u8(head, m3u8)
    if not rel or rel.status_code != 200:
        logging.error(f'请求失败，状态码为: {rel.status_code if rel else "无响应"}')
        return []
    datas = rel.text.split('\n')
    m3u8_base = m3u8[:m3u8.rfind('/') + 1]
    if len(datas) < 5:
        cache = [i for i, x in enumerate(datas) if x.find('.m3u8') != -1][0]
        cache = datas[cache]
        if cache[0:4] == 'http':
            m3u8_next = cache
        else:
            m3u8_next = m3u8_base + cache
        logging.info('发现子m3u8等待10s后继续')
        logging.info(f'm3u8地址为 : {m3u8_next}')
        time.sleep(10)
        return get_ts_list(head, m3u8_next)
    else:
        return parse_ts_list(m3u8, rel.text)
