import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


FILE_COUNT = 30  # 処理するファイル数
FILE_SIZE = 10 * 1024 * 1024  # 1MBのファイルを作成


def file_io_task(index):
    """ファイルにデータを書き込み、読み込む処理"""
    filename = f"test_file_{index}.txt"

    # 書き込み
    with open(filename, "wb") as f:
        f.write(os.urandom(FILE_SIZE))  # 1MBのランダムデータを書き込む

    # 読み込み
    with open(filename, "rb") as f:
        f.read()

    os.remove(filename)  # 後始末で削除


def run_baseline():
    """シングルスレッドで実行（Baseline）"""
    for i in range(FILE_COUNT):
        file_io_task(i)


def run_threads():
    """スレッドプールを使ってファイルI/Oを並列実行"""
    with ThreadPoolExecutor(max_workers=FILE_COUNT) as executor:
        executor.map(file_io_task, range(FILE_COUNT))


def run_processes():
    """プロセスプールを使ってファイルI/Oを並列実行"""
    with ProcessPoolExecutor(max_workers=FILE_COUNT) as executor:
        executor.map(file_io_task, range(FILE_COUNT))


if __name__ == "__main__":
    # Baseline (シングルスレッド)
    print("Starting file I/O tasks (Baseline - Single Threaded)...")
    start = time.perf_counter()
    run_baseline()
    print("Baseline time: {:.4f} sec".format(time.perf_counter() - start))

    print("-" * 100)

    # マルチスレッド
    print("Starting file I/O tasks with threads...")
    start = time.perf_counter()
    run_threads()
    print("Threads time: {:.4f} sec".format(time.perf_counter() - start))

    print("-" * 100)

    # マルチプロセス
    print("Starting file I/O tasks with processes...")
    start = time.perf_counter()
    run_processes()
    print("Processes time: {:.4f} sec".format(time.perf_counter() - start))
