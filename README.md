# shuangmians-DownReel-tool

## 项目简介
`shuangmians-DownReel-tool` 是一个高效的影视资源抓取与下载工具，支持从指定网站搜索影视资源、解析 m3u8 文件、下载 TS 文件并合并为 MP4 文件。该工具旨在提供简单易用的界面和高效的下载体验。

## 功能特性
- **影视资源搜索**：通过关键词搜索影视资源。
- **多线程下载**：支持多线程下载 TS 文件，提升下载速度。
- **自动合并**：下载完成后自动将 TS 文件合并为 MP4 文件。
- **失败重试**：支持下载失败的任务自动重试。
- **用户友好**：提供清晰的交互界面，便于用户操作。

## 环境依赖
在运行本项目之前，请确保您的环境满足以下要求：
- Python 3.7 或更高版本
- 必要的依赖库（见下方安装步骤）

## 安装步骤
1. 克隆项目到本地：
   ```bash
   git clone https://github.com/your-repo/shuangmians-DownReel-tool.git
   cd shuangmians-DownReel-tool
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置初始化文件：
   确保 `init.ini` 文件存在并正确配置下载路径和其他参数。

## 使用方法
1. 运行主程序：
   ```bash
   python main.py
   ```

2. 按照提示输入影视名称，选择资源和集数。

3. 等待下载完成，MP4 文件将保存在指定的下载路径中。

## 配置说明
配置文件 `init.ini` 包含以下设置：
- **下载路径**：`dow_path`，指定下载的文件保存路径。
- **下载并发**：`n`，设置同时下载的线程数。
- **User-Agent**：`user-agent`，用于模拟浏览器请求。

## 文件结构
```
github_pachong/
├── dow_mp4.py          # TS 文件下载与合并逻辑
├── get_m3u8.py         # 解析 m3u8 文件地址
├── get_user_mover.py   # 获取用户选择的影视资源
├── get_ts_list.py      # 获取 TS 文件列表
├── get_ji.py           # 获取影视集数信息
├── get_page.py         # 获取搜索结果页数
├── main.py             # 主程序入口
├── print_banner.py     # 打印横幅信息
├── README.md           # 项目说明文档
├── requirements.txt    # 依赖库列表
├── 打包.bat            # 打包脚本
```

## 打包方法
使用 `pyinstaller` 将项目打包为单个可执行文件：
```bash
pyinstaller --icon=.\ico\shuangmian.ico --console --onefile --distpath dist --add-data "init.ini;." main.py
```

## 注意事项
- 本工具仅供学习和研究使用，请勿用于任何非法用途。
- 下载过程中可能会遇到网络问题，请确保网络连接稳定。

## 贡献
欢迎提交 Issue 和 Pull Request 来改进本项目。
