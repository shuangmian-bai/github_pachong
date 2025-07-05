import os
import shutil
import threading
import time
import logging
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
        except (ConnectionError, RequestException) as e:
            logging.warning(f"请求失败，重试 {retries + 1}/{max_retries}: {e}")
            time.sleep(backoff_factor * (retries + 1))
    logging.error(f"请求失败，达到最大重试次数: {url}")
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
            progress_bar.update(1)
        except Exception as e:
            logging.error(f"下载失败: {ts_url}, 错误: {e}")
            progress_bar.set_description(f'下载失败: {ts_url}')
            failed_urls.append(ts_url)

def download_ts_files(ts_list, output_dir, n, max_retries=3):
    """下载所有 ts 文件，支持失败任务的重新尝试"""
    semaphore = threading.Semaphore(n)
    failed_urls = []
    lens = len(str(len(ts_list)))

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
        logging.warning(f"以下 ts 文件下载失败: {failed_urls}")
    return failed_urls

def concatenate_ts_files(output_dir, output_file):
    """合并 ts 文件"""
    ts_files = sorted(
        [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.ts')]
    )
    with open(output_file, 'wb') as outfile:
        for ts_file in ts_files:
            with open(ts_file, 'rb') as infile:
                outfile.write(infile.read())

def download_and_merge(ts_list, output_dir, output_file, n):
    """下载所有 ts 并合并为 mp4"""
    failed_urls = download_ts_files(ts_list, output_dir, n)
    if not failed_urls:
        concatenate_ts_files(output_dir, output_file)
        shutil.rmtree(output_dir, ignore_errors=True)
        return True
    else:
        logging.error("部分文件下载失败，请检查网络或重试。")
        return False

def dow_mp4(ts_list, path, n):
    """主入口：下载并合并 TS 文件为 MP4"""
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    name = os.path.basename(path)
    base_path = os.path.dirname(path)
    output_dir = os.path.join(base_path, os.path.splitext(name)[0])
    output_file = os.path.join(base_path, name)
    os.makedirs(output_dir, exist_ok=True)
    download_and_merge(ts_list, output_dir, output_file, n)
