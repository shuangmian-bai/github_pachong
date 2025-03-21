#!/bin/bash

rm -rf dist
pyinstaller --icon=./ico/shuangmian.ico --console --onefile --distpath dist main.py
cp init.ini dist/
