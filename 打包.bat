rmdir /s /q dist
pyinstaller --icon=.\\ico\\shuangmian.ico --console --onefile --distpath dist main.py
copy init.ini dist\