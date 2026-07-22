"""
Task 5: Sequential, threaded, and multiprocessing parallel merge sort.
"""

import heapq
import random
import threading
import multiprocessing
import time

MAX_THREADS = 1
active_threads = 1
active_threads_lock = threading.Lock()


def merge(arr, left, mid, right):
    left_part = arr[left:mid + 1]
    right_part = arr[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1
    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1
    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1


def sequential_merge_sort(arr, left=None, right=None):
    if left is None:
        left, right = 0, len(arr) - 1
    if left >= right:
        return
    mid = left + (right - left) // 2
    sequential_merge_sort(arr, left, mid)
    sequential_merge_sort(arr, mid + 1, right)
    merge(arr, left, mid, right)


def parallel_merge_sort(arr, left, right):
    """Uses threading.Thread, guarded by active_threads_lock (the critical section)."""
    global active_threads
    if left >= right:
        return
    mid = left + (right - left) // 2

    spawn_thread = False
    with active_threads_lock:
        if active_threads < MAX_THREADS:
            active_threads += 1
            spawn_thread = True

    if spawn_thread:
        t = threading.Thread(target=parallel_merge_sort, args=(arr, left, mid))
        t.start()
        parallel_merge_sort(arr, mid + 1, right)
        t.join()
        with active_threads_lock:
            active_threads -= 1
    else:
        sequential_merge_sort(arr, left, mid)
        parallel_merge_sort(arr, mid + 1, right)

    merge(arr, left, mid, right)


def run_threaded(n, thread_budget, seed=42):
    global MAX_THREADS, active_threads
    MAX_THREADS = thread_budget
    active_threads = 1
    rnd = random.Random(seed)
    arr = [rnd.randint(0, 1_000_000_000) for _ in range(n)]
    t0 = time.perf_counter()
    parallel_merge_sort(arr, 0, n - 1)
    elapsed = time.perf_counter() - t0
    assert all(arr[i] <= arr[i + 1] for i in range(n - 1)), "sort failed"
    return elapsed, arr


def run_sequential(n, seed=42):
    rnd = random.Random(seed)
    arr = [rnd.randint(0, 1_000_000_000) for _ in range(n)]
    t0 = time.perf_counter()
    sequential_merge_sort(arr)
    elapsed = time.perf_counter() - t0
    return elapsed, arr


def _mp_sort_chunk(chunk):
    chunk = list(chunk)
    sequential_merge_sort(chunk)
    return chunk


def _merge_two_sorted(a, b):
    return list(heapq.merge(a, b))


def run_multiprocessing(n, n_procs, seed=42):
    rnd = random.Random(seed)
    arr = [rnd.randint(0, 1_000_000_000) for _ in range(n)]
    chunk_size = (n + n_procs - 1) // n_procs
    chunks = [arr[i:i + chunk_size] for i in range(0, n, chunk_size)]

    t0 = time.perf_counter()
    with multiprocessing.Pool(processes=n_procs) as pool:
        sorted_chunks = pool.map(_mp_sort_chunk, chunks)
    merged = sorted_chunks[0]
    for c in sorted_chunks[1:]:
        merged = _merge_two_sorted(merged, c)
    elapsed = time.perf_counter() - t0
    assert all(merged[i] <= merged[i + 1] for i in range(len(merged) - 1))
    return elapsed, merged
