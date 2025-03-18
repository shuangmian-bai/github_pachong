import os
import time
import logging
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dow_mp4 import dow_mp4
from get_page import get_page
from get_user_mover import get_user_mover
from get_ji import get_ji
from get_ts_list import get_ts_list
from get_m3u8 import get_m3u8

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 读取配置文件，指定编码为 utf-8
config = configparser.ConfigParser()
config.read('init.ini', encoding='utf-8')

# 从配置文件中读取变量
dow_path = config['Settings']['dow_path']
n = int(config['Settings']['n'])
chrome_path = config['Settings']['chrome_path']
chromedriver_path = config['Settings']['chromedriver_path']

def main():
    path = 'https://www.cbh1.cc'
    url = f'{path}/search/index.html'

    # 设置浏览器选项
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式
    options.binary_location = chrome_path  # 指定 Chrome 浏览器的路径

    # 新建浏览器对象
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

    try:
        # 输入关键词
        name = input('请输入想看的影视名 : ')

        # 获取总页码
        pages = get_page(head, url, name)

        #https://www.cbh1.cc/public/auto/search1.html?keyword=%E5%8C%97%E4%B8%8A&page=1
        # 生成url2列表
        url2_list = [f'https://www.cbh1.cc/public/auto/search1.html?keyword={name}&page={x}' for x in range(1, pages + 1)]

        # 获取用户选择影视, 视频播放地址为url2, 并且重新定义一下name
        sj = get_user_mover(driver, url2_list)

        # 清空控制台
        print("\033c", end="")

        url2 = sj['url']
        url2 = f'{path}{url2}'
        name = sj['name']

        # 获取用户选集数据
        ji_list = get_ji(head, url2)

        # 把选集的完整url填充
        ji_list = {ji_list[x]: path + x for x in ji_list}

        print("\033c", end="")

        # 循环取值
        for ji_data in ji_list:
            # 如果mp4文件已经存在, 则跳过
            if os.path.exists(f'{dow_path}{name}_{ji_data}.mp4'):
                logging.info(f'{dow_path}{name}_{ji_data}.mp4 已存在, 跳过')
                continue

            # 数据提取
            url3 = ji_list[ji_data]

            # 根据分析, 视频播放为m3u8播放格式

            # 获取m3u8
            m3u8 = get_m3u8(head, url3)
            print('m3u8地址为 : ', m3u8)

            # 解析m3u8
            ts_list = get_ts_list(driver, m3u8)

            dow_mp4(ts_list, f'{dow_path}{name}_{ji_data}.mp4', n)

            # 下载间隔控制
            time.sleep(10)

    except Exception as e:
        logging.error(f'程序运行时发生错误: {e}')
    finally:
        # 关闭浏览器驱动
        driver.quit()
        logging.info('浏览器驱动已关闭')

if __name__ == '__main__':
    head = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'priority':'u=0, i',
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
    main()
