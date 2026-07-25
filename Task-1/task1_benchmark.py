"""
Task 1: Empirical benchmark for BST, AVL Tree, Min-Heap, Hash Table.
Standalone script - does not modify structures.py or task1_menu.py.

Run it, type an N (e.g. 100), see the timing table, then type another N
(e.g. 1000, then 10000) to keep testing without restarting the script.
Type 'done' when finished to get a summary table and a comparison chart.
"""

import random
import time
from structures import City, BST, AVLTree, MinHeap, HashTable

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def make_cities(n, seed):
    rnd = random.Random(seed)
    cities = []
    for i in range(n):
        cities.append(City(
            name=f"City{i}",
            x=round(rnd.uniform(0, 1000), 1),
            y=round(rnd.uniform(0, 1000), 1),
            population=rnd.randint(1000, 2_000_000),
            distance=round(rnd.uniform(0, 1000), 1),
        ))
    return cities


def benchmark(n, repeats=3, seed_base=100):
    """Times insert/search/delete for all four structures at size n,
    averaged over `repeats` runs. Search/delete use a sample of up to
    200 items (not all n) so timing stays fast even at n=10,000."""
    keys = [
        "bst_insert", "bst_search", "bst_delete",
        "avl_insert", "avl_search", "avl_delete",
        "heap_push", "heap_pop",
        "hash_insert", "hash_search", "hash_delete",
    ]
    totals = {k: [] for k in keys}

    for r in range(repeats):
        cities = make_cities(n, seed_base + r)
        sample_size = min(200, n)
        sample = random.Random(seed_base + r + 1000).sample(cities, sample_size)

        bst = BST()
        t0 = time.perf_counter()
        for c in cities:
            bst.insert(c.distance, c)
        totals["bst_insert"].append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        for c in sample:
            bst.search(c.distance)
        totals["bst_search"].append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        for c in sample:
            bst.delete(c.distance)
        totals["bst_delete"].append(time.perf_counter() - t0)

        avl = AVLTree()
        t0 = time.perf_counter()
        for c in cities:
            avl.insert(c.distance, c)
        totals["avl_insert"].append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        for c in sample:
            avl.search(c.distance)
        totals["avl_search"].append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        for c in sample:
            avl.delete(c.distance)
        totals["avl_delete"].append(time.perf_counter() - t0)

        heap = MinHeap()
        t0 = time.perf_counter()
        for c in cities:
            heap.push(c.distance, c)
        totals["heap_push"].append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        for _ in range(sample_size):
            if len(heap):
                heap.pop()
        totals["heap_pop"].append(time.perf_counter() - t0)

        ht = HashTable()
        t0 = time.perf_counter()
        for c in cities:
            ht.insert(c.name, c)
        totals["hash_insert"].append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        for c in sample:
            ht.search(c.name)
        totals["hash_search"].append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        for c in sample:
            ht.delete(c.name)
        totals["hash_delete"].append(time.perf_counter() - t0)

    return {k: sum(v) / len(v) for k, v in totals.items()}


def print_results(n, results):
    print(f"\n--- Results for N={n} (averaged over 3 runs) ---")
    print(f"{'Operation':16s}{'Time (ms)':>12s}")
    for key, val in results.items():
        print(f"{key:16s}{val * 1000:12.4f}")


def plot_results(all_results):
    if not HAS_MATPLOTLIB:
        print("\nmatplotlib not installed - skipping chart. Run: pip install matplotlib")
        return
    ns = sorted(all_results.keys())
    if len(ns) < 2:
        print("\nNeed at least 2 different N values tested to draw a comparison chart.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    ax = axes[0]
    for key, label in [("bst_insert", "BST"), ("avl_insert", "AVL"),
                        ("hash_insert", "Hash Table"), ("heap_push", "Min-Heap")]:
        ax.plot(ns, [all_results[n][key] * 1000 for n in ns], marker='o', label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('N (number of cities)')
    ax.set_ylabel('Total insert time (ms)')
    ax.set_title('Insertion time vs N (log-log)')
    ax.legend(fontsize=8)
    ax.grid(True, which='both', alpha=0.3)

    ax = axes[1]
    for key, label in [("bst_search", "BST"), ("avl_search", "AVL"), ("hash_search", "Hash Table")]:
        ax.plot(ns, [all_results[n][key] * 1000 for n in ns], marker='o', label=label)
    ax.set_xscale('log')
    ax.set_xlabel('N (number of cities)')
    ax.set_ylabel('Search time (ms, sampled lookups)')
    ax.set_title('Search time vs N (log-x)')
    ax.legend(fontsize=8)
    ax.grid(True, which='both', alpha=0.3)

    plt.tight_layout()
    plt.savefig("task1_benchmark_chart.png", dpi=150)
    print("\nChart saved as task1_benchmark_chart.png")


def main():
    all_results = {}
    print("===== Task 1: Empirical Benchmark =====")
    print("BST, AVL Tree, Min-Heap, Hash Table")
    print("Brief asks for N = 100, 1,000, and 10,000 - but you can test any N.")

    while True:
        raw = input("\nEnter N (number of cities) to test, or 'done' to finish: ").strip()
        if raw.lower() == "done":
            break
        try:
            n = int(raw)
        except ValueError:
            print("Please enter a whole number, or 'done'.")
            continue
        if n <= 0:
            print("N must be a positive number.")
            continue

        print(f"Running benchmark for N={n} (this may take a moment for large N)...")
        results = benchmark(n)
        all_results[n] = results
        print_results(n, results)

    if all_results:
        print("\n===== Summary: all N values tested =====")
        for n in sorted(all_results.keys()):
            print_results(n, all_results[n])
        plot_results(all_results)
    else:
        print("No benchmarks were run.")


if __name__ == "__main__":
    main()
