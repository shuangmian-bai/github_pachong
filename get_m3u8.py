from bs4 import BeautifulSoup
import requests
import time

def get_m3u8(driver, url):
    # 忽略ssl警告
    requests.packages.urllib3.disable_warnings()

    # 对地址发送请求
    driver.get(url)
    time.sleep(1)

    # 使用BeautifulSoup解析页面内容
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # 解析iframe
    url2 = soup.select('#custom_player_box')[0].select('iframe')[0].attrs['src']

    # 对url2进行深解析
    url2 = url2.split('?')[-1]
    m3u8 = url2[4:]

    return m3u8