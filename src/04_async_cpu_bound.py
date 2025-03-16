import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def cpu_bound_task(n: int) -> int:
    """CPU負荷の高いタスク"""
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


async def async_cpu_task(n: int):
    """非同期でCPUバウンドな処理を実行（GILの影響で並列化されない）"""
    return cpu_bound_task(n)  # 通常の関数をそのまま呼ぶ


async def run_async(n: int, repeat: int):
    """asyncio で CPU バウンドタスクを実行（並列化されないことを確認）"""
    tasks = [async_cpu_task(repeat) for _ in range(n)]
    results = await asyncio.gather(*tasks)
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

    print("Starting CPU-bound tasks with asyncio (Expected to be slow)...")
    start = time.perf_counter()
    asyncio.run(run_async(num_tasks, repeat))
    print("Async time: {:.4f} sec".format(time.perf_counter() - start))
