#!/bin/bash

rm -rf dist
pyinstaller --icon=./ico/shuangmian.ico --console --onefile --distpath dist --add-data "init.ini:." --name "双面的影视爬虫" main.py
