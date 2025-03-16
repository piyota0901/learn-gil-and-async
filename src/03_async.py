import os
import time
import asyncio
import aiofiles
import httpx
from concurrent.futures import ThreadPoolExecutor

FILE_COUNT = 10  # 処理するファイル数
FILE_SIZE = 1024 * 1024  # 1MB のファイルを作成
API_URL = "https://jsonplaceholder.typicode.com/todos/"  # ダミーAPI

# ---- シングルスレッド（直列処理） ----
def sync_io_task(index):
    """同期的にファイルI/OとAPIリクエストを実行"""
    filename = f"sync_test_file_{index}.txt"

    # ファイル書き込み
    with open(filename, "wb") as f:
        f.write(os.urandom(FILE_SIZE))

    # ファイル読み込み
    with open(filename, "rb") as f:
        f.read()

    os.remove(filename)

    # APIリクエスト（同期処理）
    response = httpx.get(f"{API_URL}{index}")
    return response.status_code

def run_sync():
    """シングルスレッドで処理"""
    for i in range(FILE_COUNT):
        sync_io_task(i)


# ---- マルチスレッド（ThreadPoolExecutor） ----
def run_threads():
    """スレッドを使ってファイルI/OとAPIリクエストを並列処理"""
    with ThreadPoolExecutor(max_workers=FILE_COUNT) as executor:
        results = list(executor.map(sync_io_task, range(FILE_COUNT)))
    return results


# ---- 非同期処理（asyncio + aiofiles + httpx） ----
async def async_io_task(index):
    """非同期でファイルI/OとAPIリクエストを実行"""
    filename = f"async_test_file_{index}.txt"

    # 非同期ファイル書き込み
    async with aiofiles.open(filename, "wb") as f:
        await f.write(os.urandom(FILE_SIZE))

    # 非同期ファイル読み込み
    async with aiofiles.open(filename, "rb") as f:
        await f.read()

    os.remove(filename)

    # 非同期APIリクエスト
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}{index}")

    return response.status_code

async def run_async():
    """asyncioを使って非同期で処理"""
    tasks = [async_io_task(i) for i in range(FILE_COUNT)]
    results = await asyncio.gather(*tasks)
    return results


# ---- 実行テスト ----
if __name__ == "__main__":
    print("Starting synchronous tasks (Single Thread)...")
    start = time.perf_counter()
    run_sync()
    print("Sync time: {:.4f} sec".format(time.perf_counter() - start))

    print("-" * 100)

    print("Starting file I/O tasks with threads...")
    start = time.perf_counter()
    run_threads()
    print("Threads time: {:.4f} sec".format(time.perf_counter() - start))

    print("-" * 100)

    print("Starting file I/O tasks with asyncio...")
    start = time.perf_counter()
    asyncio.run(run_async())
    print("Async time: {:.4f} sec".format(time.perf_counter() - start))
