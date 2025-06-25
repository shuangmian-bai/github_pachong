import os
import time
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

def get_config_path():
    if getattr(sys, 'frozen', False):
        config_dir = os.path.expanduser('~/.github_pachong')
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, 'init.ini')
    else:
        config_path = 'init.ini'
    return config_path

def get_default_config_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'init.ini')
    else:
        return 'init.ini'

config_path = get_config_path()
default_config_path = get_default_config_path()

if not os.path.exists(config_path):
    shutil.copy(default_config_path, config_path)

config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')

DEFAULT_DOW_PATH = './下载/'
DEFAULT_N = 150
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'

DOW_PATH = config.get('Settings', 'dow_path', fallback=DEFAULT_DOW_PATH)
N = config.getint('Settings', 'n', fallback=DEFAULT_N)

head = {
    'user-agent': config.get('Head', 'user-agent', fallback=DEFAULT_USER_AGENT)
}

def clear_console():
    print("\033c", end="")
    print_banner()

def get_search_pages(head, url, name):
    try:
        return get_page(head, url, name)
    except Exception:
        return 1

def generate_search_urls(name, pages):
    return [SEARCH_PAGE_URL_TEMPLATE.format(x, name) for x in range(1, pages + 1)]

def get_video_info(head, url2_list):
    try:
        return get_user_mover(head, url2_list)
    except Exception:
        raise

def get_episode_list(head, url2):
    try:
        return get_ji(head, url2)
    except Exception:
        raise

def download_video(ts_list, file_path, n):
    try:
        dow_mp4(ts_list, file_path, n)
    except Exception:
        raise

def validate_input(prompt, valid_choices=None, cast_type=str):
    """通用输入验证函数"""
    while True:
        try:
            user_input = cast_type(input(prompt).strip())
            if valid_choices and user_input not in valid_choices:
                print(f"无效输入，请输入以下选项之一: {valid_choices}")
                continue
            return user_input
        except ValueError:
            print(f"无效输入，请输入正确的 {cast_type.__name__} 类型值。")


def print_banner():
    banner = """
 _______  _______  _______  _______  _______  _______  _______
(  ____ $\\/(      (  ____ \\(  ___  )(       )(  ____ $$(  ____ \\
| (    \\/| () () | (    \\/| (   ) || () () || (    \\/| (    \\/
| (__    | || || | (__    | (___) || || || || (__    | (_____
|  __)   | |(_)| |  __)   |  ___  || |(_)| ||  __)   (_____  \\
| (      | |   | | (      | (   ) || |   | || (            ) |
| (____/\\| )   ( | (____/\\| )   ( || )   ( || (____/\\/\\____) |
(_______/|/     \\(_______/|/     \\||/     \\|(_______/\\_______)

    """
    print(banner)
    print("工具名称: shuangmians-DownReel-tool")
    print("作者名称: 双面")
    print("版本信息: v1.0.0")
    print("功能描述: 高效影视资源抓取与下载工具")
    print("=" * 80)

def main():
    try:
        clear_console()
        print("=" * 50 + " 用户选择下载影视 " + "=" * 50)
        name = input('请输入想看的影视名 : ').strip()
        if not name:
            print("影视名不能为空！")
            return

        cache = SEARCH_PAGE_URL_TEMPLATE.format(1, name)
        pages = get_search_pages(head, cache, name)
        if pages == 1:
            print("未找到相关影视资源。")
            return

        clear_console()
        print(f"找到 {pages} 页相关影视资源。")

        url2_list = generate_search_urls(name, pages)
        sj = get_video_info(head, url2_list)
        clear_console()

        url2 = f'{BASE_URL}{sj["url"]}'
        name = sj['name']

        ji_list = get_episode_list(head, url2)
        ji_list = {ji_list[x]: BASE_URL + x for x in ji_list}

        clear_console()

        for ji_data, url3 in ji_list.items():
            file_path = f'{DOW_PATH}{name}_{ji_data}.mp4'
            if os.path.exists(file_path):
                print(f"文件已存在，跳过: {file_path}")
                continue

            print(f'-----------{name}{ji_data}----------------------')
            m3u8 = get_m3u8(head, url3)
            print('m3u8地址为', m3u8)

            try:
                ts_list = get_ts_list(head, m3u8)
                if not ts_list:
                    print("未找到 ts 文件列表，跳过当前集。")
                    continue
                download_video(ts_list, file_path, N)
            except Exception as e:
                print(f"下载失败: {e}")

            time.sleep(10)

    except Exception as e:
        print(f"程序运行时发生错误: {e}")

def settings_menu(config, config_path):
    while True:
        clear_console()
        print("=" * 50 + " 用户设置 " + "=" * 50)
        print('0 设置下载路径')
        print('1 设置下载并发')
        print('2 返回主菜单')
        print("=" * 80)
        choice = validate_input('请输入 : ', valid_choices=[0, 1, 2], cast_type=int)

        if choice == 0:
            current_path = config.get('Settings', 'dow_path', fallback=DEFAULT_DOW_PATH)
            print('当前路径为 : ', current_path)
            new_path = input('请输入下载路径 : ')

            new_path = new_path.replace('\\', '/').rstrip('/') + '/'
            config.set('Settings', 'dow_path', new_path)
        elif choice == 1:
            current_n = config.getint('Settings', 'n', fallback=DEFAULT_N)
            print('当前并发为 : ', current_n)
            new_n = validate_input('请输入下载并发 : ', cast_type=int)
            config.set('Settings', 'n', str(new_n))
        elif choice == 2:
            return

        with open(config_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

if __name__ == '__main__':
    while True:
        clear_console()
        print_banner()
        print("=" * 30 + " 选项主菜单 " + "=" * 30)
        print('请输入您需要的操作')
        print('0 开始爬取')
        print('1 设置')
        print('2 退出')
        print("=" * 70)
        choice = validate_input('请输入 : ', valid_choices=[0, 1, 2], cast_type=int)

        if choice == 0:
            main()
        elif choice == 1:
            settings_menu(config, config_path)
        elif choice == 2:
            sys.exit(0)
