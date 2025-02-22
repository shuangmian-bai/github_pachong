import os
import shutil
import threading
import time
import requests
from requests.exceptions import RequestException, ConnectionError
from tqdm import tqdm
import logging
import subprocess

# 手动创建日志文件并设置编码
log_file = 'dow_mp4.log'
with open(log_file, 'w', encoding='utf-8') as f:
    pass

# 配置日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建文件处理器并设置编码
file_handler = logging.FileHandler(log_file, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将文件处理器添加到日志记录器
logger.addHandler(file_handler)


def retry_request(url, max_retries=3, backoff_factor=5):
    """尝试请求 URL，直到成功或达到最大重试次数"""
    session = requests.Session()
    retries = 0

    while retries < max_retries:
        try:
            response = session.get(url, timeout=10, verify=False)
            response.raise_for_status()  # 如果响应状态码不是 200，抛出异常
            return response
        except (ConnectionError, RequestException) as e:
            retries += 1
            if retries < max_retries:
                logging.error(f'请求失败: {url} (异常: {e}), 重试 {retries}/{max_retries}')
                time.sleep(backoff_factor)
            else:
                logging.error(f'请求失败: {url} (异常: {e}), 已达到最大重试次数')
                raise


def download_ts(ts_url, file_path, semaphore, failed_urls, progress_bar):
    """下载单个 ts 文件"""
    with semaphore:
        try:
            response = retry_request(ts_url)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            progress_bar.set_description(f'下载完成: {file_path}')
            progress_bar.update(1)  # 更新进度条
            logging.info(f'下载完成: {file_path}')
        except Exception as e:
            progress_bar.set_description(f'下载失败: {ts_url} (异常: {e})')
            failed_urls.append(ts_url)
            logging.error(f'下载失败: {ts_url} (异常: {e})')


def download_ts_files(ts_list, output_dir, n):
    """下载所有 ts 文件"""
    semaphore = threading.Semaphore(n)
    failed_urls = []

    # 计算文件名长度
    lens = len(str(len(ts_list)))

    threads = []
    with tqdm(total=len(ts_list), desc='下载进度') as progress_bar:
        for i, ts in enumerate(ts_list):
            ts_name = str(i).zfill(lens)
            file_path = os.path.join(output_dir, f'{ts_name}.ts')

            # 检查文件是否存在
            if os.path.exists(file_path):
                progress_bar.set_description(f'文件已存在: {file_path}')
                progress_bar.update(1)  # 更新进度条
                logging.info(f'文件已存在: {file_path}')
                continue

            # 创建线程对象
            t = threading.Thread(target=download_ts, args=(ts, file_path, semaphore, failed_urls, progress_bar))
            t.start()
            threads.append(t)

            # 每启动 n 个线程后等待 5 秒
            if (i + 1) % n == 0:
                time.sleep(5)

        # 等待所有线程完成
        for t in threads:
            t.join()

    return failed_urls


def concatenate_ts_files(output_dir, output_file):
    """使用 Windows 的 copy 命令合并 ts 文件"""
    hc = f'copy /b {output_dir}\\*.ts {output_file}'
    try:
        subprocess.run(
            hc,
            shell=True,
            check=True,
            stdout=subprocess.DEVNULL,  # 忽略标准输出
            stderr=subprocess.DEVNULL   # 忽略标准错误
        )
        logging.info(f'文件合并完成: {output_file}')
    except subprocess.CalledProcessError as e:
        logging.error(f'文件合并失败: {e}')


def dow_mp4(ts_list, path, n):
    # 从参数中提取数据
    name = os.path.basename(path)
    base_path = os.path.dirname(path)
    output_dir = os.path.join(base_path, name[:-4])
    output_file = os.path.join(base_path, name)

    # 确认路径存在
    os.makedirs(output_dir, exist_ok=True)

    # 下载 ts 文件
    failed_urls = download_ts_files(ts_list, output_dir, n)

    # 检查下载结果
    if failed_urls:
        logging.error('\n以下文件下载失败:')
        for url in failed_urls:
            logging.error(url)
    else:
        logging.info('\n所有文件下载成功')
        # 合成 mp4 文件
        concatenate_ts_files(output_dir, output_file)
        # 删除 ts 文件
        shutil.rmtree(output_dir)
