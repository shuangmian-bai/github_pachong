@echo off
setlocal

echo 正在检查 dist 目录...
if exist dist (
    rmdir /s /q dist
    echo 已删除 dist 目录
)

where pyinstaller >nul 2>nul
if errorlevel 1 (
    echo 未检测到 pyinstaller，请先安装：pip install pyinstaller
    pause
    exit /b 1
)

echo 正在打包...
pyinstaller --icon=.\ico\shuangmian.ico --console --onefile --distpath dist --add-data "init.ini;." main.py

echo 正在清理 spec 文件...
del /q /f *.spec 2>nul

echo 正在清理 build 目录...
rmdir /s /q build 2>nul

echo 打包完成！
pause
endlocal
