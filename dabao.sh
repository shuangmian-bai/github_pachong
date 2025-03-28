#!/bin/bash

rm -rf dist
pyinstaller --icon=./ico/shuangmian.ico --console --onefile --distpath dist --add-data "init.ini:." main.py
