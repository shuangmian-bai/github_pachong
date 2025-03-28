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
import sys
import shutil

# 常量定义
BASE_URL = 'https://www.bnjxjd.com'
SEARCH_URL = f'{BASE_URL}/vodsearch.html'
cache = SEARCH_URL.replace('.html', '')
SEARCH_PAGE_URL_TEMPLATE = f'{cache}/page/{{}}/wd/{{}}.html'

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_config_path():
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件，使用用户目录下的配置文件
        config_dir = os.path.expanduser('~/.github_pachong')
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, 'init.ini')
    else:
        # 如果是源代码，使用当前目录
        config_path = 'init.ini'
    return config_path

def get_default_config_path():
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件，使用临时目录中的默认配置文件
        return os.path.join(sys._MEIPASS, 'init.ini')
    else:
        # 如果是源代码，使用当前目录中的默认配置文件
        return 'init.ini'

# 读取配置文件，指定编码为 utf-8
config_path = get_config_path()
default_config_path = get_default_config_path()

if not os.path.exists(config_path):
    # 如果配置文件不存在，则从默认配置文件复制
    shutil.copy(default_config_path, config_path)

config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')

# 默认值
DEFAULT_DOW_PATH = './下载/'
DEFAULT_N = 150
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'

# 从配置文件中读取变量，如果不存在则使用默认值
DOW_PATH = config.get('Settings', 'dow_path', fallback=DEFAULT_DOW_PATH)
N = config.getint('Settings', 'n', fallback=DEFAULT_N)

# 从配置文件中读取 head 参数，如果不存在则使用默认值
head = {
    'user-agent': config.get('Head', 'user-agent', fallback=DEFAULT_USER_AGENT)
}

def clear_console():
    print("\033c", end="")

def get_search_pages(head, url, name):
    try:
        return get_page(head, url, name)
    except Exception as e:
        return 1

def generate_search_urls(name, pages):
    return [SEARCH_PAGE_URL_TEMPLATE.format(x, name) for x in range(1, pages + 1)]

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
    try:
        # 输入关键词
        name = input('请输入想看的影视名 : ')

        cache = SEARCH_PAGE_URL_TEMPLATE.format(1, name)
        # 获取总页码
        pages = get_search_pages(head, cache, name)

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
            if ts_list == []:
                print('发生意外,未获取到ts列表,请查看日志')
            else:
                download_video(ts_list, file_path, N)

            # 下载间隔控制
            time.sleep(10)

    except Exception as e:
        logging.error(f'程序运行时发生错误: {e}')


def settings_menu(config, config_path):
    while True:
        print('-----------------------------------------')
        print('0 设置下载路径')
        print('1 设置下载并发')
        print('2 退出')
        choice = input('请输入 : ')

        try:
            choice = int(choice)
        except ValueError:
            print('无效的输入，请输入数字 0, 1 或 2。')
            continue

        if choice == 0:
            current_path = config.get('Settings', 'dow_path', fallback=DEFAULT_DOW_PATH)
            print('当前路径为 : ', current_path)
            new_path = input('请输入下载路径 : ')

            new_path = new_path.replace('\\', '/').rstrip('/') + '/'
            config.set('Settings', 'dow_path', new_path)
        elif choice == 1:
            current_n = config.getint('Settings', 'n', fallback=DEFAULT_N)
            print('当前并发为 : ', current_n)
            new_n = input('请输入下载并发 : ')

            try:
                new_n = int(new_n)
                config.set('Settings', 'n', str(new_n))
            except ValueError:
                print('无效的并发数，请输入一个整数。')
                continue
        elif choice == 2:
            break
        else:
            print('无效的选择，请重新输入。')

        with open(config_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)


if __name__ == '__main__':
    print('欢迎使用双面的影视爬虫,资源均来自于第三方接口,其中广告请勿相信!!')
    print('请输入您需要的操作')
    print('0 开始爬取')
    print('1 设置')
    choice = input('请输入 : ')

    try:
        choice = int(choice)
    except ValueError:
        print('无效的输入，请输入数字 0 或 1。')
        sys.exit(1)

    if choice == 0:
        main()
    elif choice == 1:
        settings_menu(config, config_path)
    else:
        print('无效的选择，请重新输入。')
        sys.exit(1)

    main()
