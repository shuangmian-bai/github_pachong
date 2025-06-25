import time
import requests

from bs4 import BeautifulSoup

def validate_input(prompt, cast_type=str):
    while True:
        try:
            return cast_type(input(prompt))
        except ValueError:
            print('输入无效，请重新输入。')

def clear_console():
    print("\033c", end="")

def print_banner():
    print("欢迎使用影视选择器！")

def get_user_mover(head, url_list):
    #计数器,记录当前页码
    indexs = 0
    while True:
        clear_console()
        print_banner()
        # 请求页
        req = requests.get(url_list[indexs], headers=head).text
        # print(url_list[indexs])

        # 新建bs4对象
        soup = BeautifulSoup(req, 'html.parser')

        # 获取这一页所存在的影视
        datas = soup.select('.stui-vodlist.clearfix')[0].select('li')

        for i in range(len(datas)):
            data = datas[i]
            cache = data.select('.stui-vodlist__thumb.lazyload')[0]
            name = cache.get('title')
            cache = [j.select('b')[0].text for j in cache.select('span')[1:]]
            # 使用 ''.join() 方法将列表中的元素拼接成一个字符串
            name = name + '__' + '__'.join(cache)
            print(f'{i} : {name}')
        if indexs != 0:
            print('w : 上一页')

        if indexs != len(url_list)-1:
            print('s : 下一页')

        cz = validate_input('请输入您选择的操作或者需要下载的影视 : ', cast_type=str).strip()
        clear_console()
        print_banner()

        #获取操作码执行操作
        if cz.upper() == 'W':
            indexs = max(0, indexs - 1)
        elif cz.upper() == 'S':
            indexs = min(len(url_list) - 1, indexs + 1)
        else:
            try:
                cz = int(cz)
                if 0 <= cz < len(datas):
                    root = soup.select('.col-md-6.col-sm-4.col-xs-3')[cz]
                    url = root.select('.stui-vodlist__thumb.lazyload')[0].get('href')
                    name = root.select('.stui-vodlist__thumb.lazyload')[0].get('title')
                    return {'name': name, 'url': url}
                else:
                    print('输入的序号无效，请重新输入。')
            except ValueError:
                print('无效输入，请输入数字。')


