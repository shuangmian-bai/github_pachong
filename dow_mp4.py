import os
import shutil
import threading
import time
import requests
from requests.exceptions import RequestException, ConnectionError
from tqdm import tqdm
from urllib3.exceptions import InsecureRequestWarning

def retry_request(url, max_retries=3, backoff_factor=2):
    """尝试请求 URL，直到成功或达到最大重试次数"""
    session = requests.Session()
    for retries in range(max_retries):
        try:
            response = session.get(url, timeout=10, verify=False)
            response.raise_for_status()
            return response
        except (ConnectionError, RequestException):
            time.sleep(backoff_factor * (retries + 1))
    return None

def download_ts(ts_url, file_path, semaphore, failed_urls, progress_bar):
    """下载单个 ts 文件"""
    with semaphore:
        try:
            response = retry_request(ts_url)
            if response is None or len(response.content) == 0:
                raise Exception("Empty response")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            progress_bar.set_description(f'下载完成: {file_path}')
            progress_bar.update(1)  # 更新进度条
        except Exception:
            progress_bar.set_description(f'下载失败: {ts_url}')
            failed_urls.append(ts_url)

def download_ts_files(ts_list, output_dir, n):
    """下载所有 ts 文件"""
    semaphore = threading.Semaphore(n)
    failed_urls = []
    lens = len(str(len(ts_list)))  # 计算文件名长度

    def worker(ts_url, file_path):
        download_ts(ts_url, file_path, semaphore, failed_urls, progress_bar)

    threads = []
    with tqdm(total=len(ts_list), desc='下载进度') as progress_bar:
        for i, ts in enumerate(ts_list):
            ts_name = str(i).zfill(lens)
            file_path = os.path.join(output_dir, f'{ts_name}.ts')
            if os.path.exists(file_path):
                progress_bar.update(1)
                continue
            t = threading.Thread(target=worker, args=(ts, file_path))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    if failed_urls:
        print(f"以下 ts 文件下载失败: {failed_urls}")
    return failed_urls

def concatenate_ts_files(output_dir, output_file):
    """合并 ts 文件"""
    ts_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.ts')]
    ts_files.sort()  # 确保文件按顺序合并

    with open(output_file, 'wb') as outfile:
        for ts_file in ts_files:
            with open(ts_file, 'rb') as infile:
                outfile.write(infile.read())

def dow_mp4(ts_list, path, n):
    """主函数：下载并合并 TS 文件为 MP4"""
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    # 从参数中提取数据
    name = os.path.basename(path)
    base_path = os.path.dirname(path)
    output_dir_name = os.path.splitext(name)[0]  # 去掉扩展名
    output_dir = os.path.join(base_path, output_dir_name)
    output_file = os.path.join(base_path, name)

    # 确认路径存在
    os.makedirs(output_dir, exist_ok=True)

    # 下载 ts 文件
    failed_urls = download_ts_files(ts_list, output_dir, n)

    # 检查下载结果
    if not failed_urls:
        # 合成 mp4 文件
        concatenate_ts_files(output_dir, output_file)
        # 删除 ts 文件
        shutil.rmtree(output_dir, ignore_errors=True)
