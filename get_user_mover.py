import os
import requests
from bs4 import BeautifulSoup
from print_banner import print_banner

def validate_input(prompt, cast_type=str):
    while True:
        try:
            return cast_type(input(prompt))
        except ValueError:
            print('输入无效，请重新输入。')

def clear_console():
    print_banner()

def parse_movie_list(soup):
    """解析影视资源列表"""
    datas = soup.select('.stui-vodlist.clearfix li')
    result = []
    for i, data in enumerate(datas):
        thumb = data.select_one('.stui-vodlist__thumb.lazyload')
        if thumb:
            name = thumb.get('title')
            tags = '__'.join(tag.text for tag in thumb.select('span b'))
            result.append({'index': i, 'name': name, 'tags': tags, 'data': data})
            print(f'{i} : {name}__{tags}')
    return result

def get_user_mover(head, url_list, pages):
    index = 0
    while True:
        clear_console()
        try:
            req = requests.get(url_list[index], headers=head).text
            soup = BeautifulSoup(req, 'html.parser')
            movie_list = parse_movie_list(soup)
            
            # 如果当前页面没有找到资源
            if not movie_list:
                print('当前页面未找到相关影视资源。')
                # 检查是否还有其他页面可以浏览
                has_prev_page = index > 0
                has_next_page = index < len(url_list) - 1
                
                if not has_prev_page and not has_next_page:
                    print('没有任何相关影视资源。')
                    input('按回车键返回上一级...')
                    return None
                print(f"找到 {pages} 页相关影视资源。")
                print('\n可选操作:')
                if has_prev_page:
                    print('w : 上一页')
                if has_next_page:
                    print('s : 下一页')
                print('q : 返回主菜单')
                
                choice = validate_input('请输入操作: ', cast_type=str).strip().lower()
                if choice == 'w' and has_prev_page:
                    index -= 1
                elif choice == 's' and has_next_page:
                    index += 1
                elif choice == 'q':
                    return None
                else:
                    print('无效输入，请重新输入。')
                    continue
                continue
                
        except Exception as e:
            print(f'获取页面数据时发生错误: {e}')
            input('按回车键重试...')
            continue

        # 显示页面导航选项
        if index > 0:
            print('w : 上一页')
        if index < len(url_list) - 1:
            print('s : 下一页')
        print('q : 返回主菜单')
            
        choice = validate_input('请输入操作或选择的序号: ', cast_type=str).strip()
        
        # 处理页面导航
        if choice.lower() == 'w' and index > 0:
            index -= 1
        elif choice.lower() == 's' and index < len(url_list) - 1:
            index += 1
        elif choice.lower() == 'q':
            return None
        else:
            # 处理用户选择具体影视
            try:
                choice = int(choice)
                if 0 <= choice < len(movie_list):
                    selected = movie_list[choice]['data']
                    thumb = selected.select_one('.stui-vodlist__thumb.lazyload')
                    if thumb:
                        url = thumb.get('href')
                        name = thumb.get('title')
                        return {'name': name, 'url': url}
                    else:
                        print('选择的影视资源信息不完整，请重新选择。')
                else:
                    print('输入的序号无效，请重新输入。')
            except ValueError:
                print('无效输入，请输入数字或操作符。')