rmdir /s /q dist
pyinstaller --icon=.\\ico\\shuangmian.ico --console --distpath dist main.py
copy init.ini dist\main\