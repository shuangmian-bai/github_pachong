import os
import time
import requests

from bs4 import BeautifulSoup
from print_banner import print_banner  # 导入封装的 print_banner 函数

def validate_input(prompt, cast_type=str):
    while True:
        try:
            return cast_type(input(prompt))
        except ValueError:
            print('输入无效，请重新输入。')

def clear_console():
    os.system('cls')  # 使用系统命令清屏
    print_banner()

def get_user_mover(head, url_list, pages):
    """获取用户选择的影视资源"""
    index = 0
    while True:
        clear_console()
        print(f"找到 {pages} 页相关影视资源。")
        req = requests.get(url_list[index], headers=head).text
        soup = BeautifulSoup(req, 'html.parser')
        datas = soup.select('.stui-vodlist.clearfix li')

        for i, data in enumerate(datas):
            thumb = data.select_one('.stui-vodlist__thumb.lazyload')
            name = thumb.get('title')
            tags = '__'.join(tag.text for tag in thumb.select('span b'))
            print(f'{i} : {name}__{tags}')

        if index > 0:
            print('w : 上一页')
        if index < len(url_list) - 1:
            print('s : 下一页')

        choice = validate_input('请输入操作或选择的序号: ', cast_type=str).strip()
        if choice.lower() == 'w' and index > 0:
            index -= 1
        elif choice.lower() == 's' and index < len(url_list) - 1:
            index += 1
        else:
            try:
                choice = int(choice)
                if 0 <= choice < len(datas):
                    selected = datas[choice]
                    url = selected.select_one('.stui-vodlist__thumb.lazyload').get('href')
                    name = selected.select_one('.stui-vodlist__thumb.lazyload').get('title')
                    return {'name': name, 'url': url}
                else:
                    print('输入的序号无效，请重新输入。')
            except ValueError:
                print('无效输入，请输入数字或操作符。')


