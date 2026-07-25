"""
Task 2: Empirical benchmark for Dijkstra, Prim, Bellman-Ford.
Standalone script - does not modify graph.py or task2_menu.py.

For each V you enter, it builds a sparse graph (E ~ 2V) and a dense
graph (E ~ V^2/4), then times all three algorithms on both, using
time.perf_counter(), averaged over 3 runs.

Run it, type a V (e.g. 50), see the results, then type another V
(e.g. 200, then 500) to keep testing without restarting the script.
Type 'done' when finished to get a summary table and a comparison chart.
"""
import time
from graph import random_graph, dijkstra, prim_mst, bellman_ford

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

def benchmark(v, reps=3, seed_base=1000):
    """Times Dijkstra, Prim, Bellman-Ford on a sparse and a dense random
    graph with v nodes, averaged over `reps` runs."""
    sparse_edges = v * 2
    dense_edges = v * (v - 1) // 4

    results = {"sparse": {"dijkstra": [], "prim": [], "bellman_ford": []},
               "dense": {"dijkstra": [], "prim": [], "bellman_ford": []}}

    for r in range(reps):
        for density, edges in [("sparse", sparse_edges), ("dense", dense_edges)]:
            g = random_graph(v, edges, seed=seed_base + r)
            src = g.nodes()[0]

            t0 = time.perf_counter()
            dijkstra(g, src)
            results[density]["dijkstra"].append(time.perf_counter() - t0)

            t0 = time.perf_counter()
            prim_mst(g, src)
            results[density]["prim"].append(time.perf_counter() - t0)

            t0 = time.perf_counter()
            bellman_ford(g, src)
            results[density]["bellman_ford"].append(time.perf_counter() - t0)

    averaged = {}
    for density in ("sparse", "dense"):
        averaged[density] = {algo: sum(vals) / len(vals) for algo, vals in results[density].items()}
    averaged["sparse_edges"] = sparse_edges
    averaged["dense_edges"] = dense_edges
    return averaged

def print_results(v, results):
    print(f"\n--- Results for V={v} (averaged over 3 runs) ---")
    print(f"Sparse graph: E={results['sparse_edges']} (~2V)")
    print(f"{'Algorithm':16s}{'Time (ms)':>12s}")
    for algo, val in results["sparse"].items():
        print(f"{algo:16s}{val * 1000:12.4f}")
    print(f"\nDense graph: E={results['dense_edges']} (~V^2/4)")
    print(f"{'Algorithm':16s}{'Time (ms)':>12s}")
    for algo, val in results["dense"].items():
        print(f"{algo:16s}{val * 1000:12.4f}")

def plot_results(all_results):
    if not HAS_MATPLOTLIB:
        print("\nmatplotlib not installed - skipping chart. Run: pip install matplotlib")
        return
    vs = sorted(all_results.keys())
    if len(vs) < 2:
        print("\nNeed at least 2 different V values tested to draw a comparison chart.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    algos = [("dijkstra", "Dijkstra"), ("prim", "Prim"), ("bellman_ford", "Bellman-Ford")]

    for ax, density in zip(axes, ["sparse", "dense"]):
        for key, label in algos:
            ax.plot(vs, [all_results[v][density][key] * 1000 for v in vs], marker='o', label=label)
        density_label = "2V" if density == "sparse" else "V\u00b2/4"
        ax.set_xlabel("V (number of nodes)")
        ax.set_ylabel("Time (ms)")
        ax.set_title(f"{density.capitalize()} graphs (E \u2248 {density_label})")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("task2_benchmark_chart.png", dpi=150)
    print("\nChart saved as task2_benchmark_chart.png")

def main():
    all_results = {}
    print("===== Task 2: Empirical Benchmark =====")
    print("Dijkstra, Prim, Bellman-Ford on sparse (E~2V) and dense (E~V^2/4) graphs")

    while True:
        raw = input("\nEnter V (number of nodes) to test, or 'done' to finish: ").strip()
        if raw.lower() == "done":
            break
        try:
            v = int(raw)
        except ValueError:
            print("Please enter a whole number, or 'done'.")
            continue
        if v < 3:
            print("V must be at least 3.")
            continue

        print(f"Running benchmark for V={v} (this may take a moment for large V)...")
        results = benchmark(v)
        all_results[v] = results
        print_results(v, results)

    if all_results:
        print("\n===== Summary: all V values tested =====")
        for v in sorted(all_results.keys()):
            print_results(v, all_results[v])
        plot_results(all_results)
    else:
        print("No benchmarks were run.")

if __name__ == "__main__":
    main()
