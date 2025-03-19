import os
import time
import logging
import configparser
from dow_mp4 import dow_mp4
from get_page import get_page
from get_user_mover import get_user_mover
from get_ji import get_ji
from get_ts_list import get_ts_list
from get_m3u8 import get_m3u8

# 常量定义
BASE_URL = 'https://www.cbh1.cc'
SEARCH_URL = f'{BASE_URL}/search/index.html'
SEARCH_PAGE_URL_TEMPLATE = f'{BASE_URL}/public/auto/search1.html?keyword={{}}&page={{}}'

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 读取配置文件，指定编码为 utf-8
config = configparser.ConfigParser()
config.read('init.ini', encoding='utf-8')

# 从配置文件中读取变量
DOW_PATH = config['Settings']['dow_path']
N = int(config['Settings']['n'])

def clear_console():
    print("\033c", end="")

def get_search_pages(head, url, name):
    try:
        return get_page(head, url, name)
    except Exception as e:
        logging.error(f'获取搜索页码时发生错误: {e}')
        raise

def generate_search_urls(name, pages):
    return [SEARCH_PAGE_URL_TEMPLATE.format(name, x) for x in range(1, pages + 1)]

def get_video_info(head, url2_list):
    try:
        return get_user_mover(head, url2_list)
    except Exception as e:
        logging.error(f'获取视频信息时发生错误: {e}')
        raise

def get_episode_list(head, url2):
    try:
        return get_ji(head, url2)
    except Exception as e:
        logging.error(f'获取选集列表时发生错误: {e}')
        raise

def download_video(ts_list, file_path, n):
    try:
        dow_mp4(ts_list, file_path, n)
    except Exception as e:
        logging.error(f'下载视频时发生错误: {e}')
        raise

def main():
    head = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
    }

    try:
        # 输入关键词
        name = input('请输入想看的影视名 : ')

        # 获取总页码
        pages = get_search_pages(head, SEARCH_URL, name)

        # 生成url2列表
        url2_list = generate_search_urls(name, pages)

        # 获取用户选择影视, 视频播放地址为url2, 并且重新定义一下name
        sj = get_video_info(head, url2_list)

        clear_console()

        url2 = sj['url']
        url2 = f'{BASE_URL}{url2}'
        name = sj['name']

        # 获取用户选集数据
        ji_list = get_episode_list(head, url2)

        # 把选集的完整url填充
        ji_list = {ji_list[x]: BASE_URL + x for x in ji_list}

        clear_console()

        # 循环取值
        for ji_data in ji_list:
            file_path = f'{DOW_PATH}{name}_{ji_data}.mp4'
            # 如果mp4文件已经存在, 则跳过
            if os.path.exists(file_path):
                logging.info(f'{file_path} 已存在, 跳过')
                continue

            # 数据提取
            url3 = ji_list[ji_data]

            # 获取m3u8
            m3u8 = get_m3u8(head, url3)
            print('m3u8地址为', m3u8)

            # 解析m3u8
            ts_list = get_ts_list(head, m3u8)

            download_video(ts_list, file_path, N)

            # 下载间隔控制
            time.sleep(10)

    except Exception as e:
        logging.error(f'程序运行时发生错误: {e}')

if __name__ == '__main__':
    main()
