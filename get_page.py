import time

from bs4 import BeautifulSoup

def get_page(driver, url, name):
    driver.get(url + "?keyword=" + name)
    time.sleep(1)

    # 使用BeautifulSoup解析页面内容
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # bs4获取最后一页
    pages = soup.select('.myci-page')[0].select('li')[-1].select('a')[0].attrs['href']
    pages = int(pages.split('=')[-1])

    return pages
