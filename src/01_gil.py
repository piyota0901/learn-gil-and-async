import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def cpu_bound_task(n: int) -> int:
    """単純な計算を繰り返してCPUを使うタスク"""
    total = 0
    for _ in range(n):
        total += 1
    return total


def run_threads(n: int, repeat: int):
    """スレッドを使ってCPUバウンドな処理を実行"""
    with ThreadPoolExecutor(max_workers=n) as executor:
        results = list(executor.map(cpu_bound_task, [repeat] * n))
    return results


def run_processes(n: int, repeat: int):
    """プロセスを使ってCPUバウンドな処理を実行"""
    with ProcessPoolExecutor(max_workers=n) as executor:
        results = list(executor.map(cpu_bound_task, [repeat] * n))
    return results


def run_processes_usin_pool(n: int, repeat: int):
    """プロセスを使ってCPUバウンドな処理を実行"""
    with ProcessPoolExecutor(max_workers=n) as executor:
        # chunksize を適切に設定（試行錯誤が必要だが、n の 1/4 〜 1/2 程度が良い）
        chunksize = max(1, n // 2)
        results = list(executor.map(cpu_bound_task, [repeat] * n, chunksize=chunksize))
    return results


if __name__ == "__main__":
    num_tasks = 4  # 並列に実行する数（CPUコア数と同じくらいが良い）
    repeat = 10**7  # 負荷をかけるためのループ回数

    print("Baseline (single-threaded)...")
    start = time.perf_counter()
    for _ in range(num_tasks):
        cpu_bound_task(repeat)
    print("Baseline time: {:.4f} sec".format(time.perf_counter() - start))

    print("-" * 100)

    print("Starting CPU-bound tasks with threads...")
    start = time.perf_counter()
    run_threads(num_tasks, repeat)
    print("Threads time: {:.4f} sec".format(time.perf_counter() - start))

    print("-" * 100)

    print("Starting CPU-bound tasks with processes...")
    start = time.perf_counter()
    run_processes(num_tasks, repeat)
    print("Processes time: {:.4f} sec".format(time.perf_counter() - start))
    
    print("-" * 100)

    print("Starting CPU-bound tasks with processes using pool...")
    start = time.perf_counter()
    run_processes(num_tasks, repeat)
    print("Processes using pool time: {:.4f} sec".format(time.perf_counter() - start))

