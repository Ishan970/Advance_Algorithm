"""
Task 2: Interactive demo for graph building + Dijkstra, Prim, Bellman-Ford.
"""

from graph import Graph, dijkstra, reconstruct_path, prim_mst, bellman_ford, random_graph


def read_float(prompt):
    try:
        return float(input(prompt).strip())
    except ValueError:
        print("Please enter a valid number.")
        return None


# Graph builder sub-menu
def run_graph_builder(g):
    print("\n--- Graph builder ---")
    while True:
        print(
            "\nGraph menu:\n"
            "  1) Add an edge (u, v, weight)\n"
            "  2) Remove an edge\n"
            "  3) Show all nodes\n"
            "  4) Show all edges\n"
            "  5) Load a random sample network\n"
            "  6) Clear the graph\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            u = input("From node: ").strip()
            v = input("To node: ").strip()
            w = read_float("Weight: ")
            if u and v and w is not None:
                g.add_edge(u, v, w)
                print(f"Added edge {u} -> {v} (weight {w})")

        elif choice == "2":
            u = input("From node: ").strip()
            v = input("To node: ").strip()
            g.remove_edge(u, v)
            print(f"Removed edge {u} -> {v} (if it existed)")

        elif choice == "3":
            nodes = g.nodes()
            print(f"({len(nodes)} nodes)" if nodes else "(no nodes yet)")
            for n in nodes:
                print(f"  {n}")

        elif choice == "4":
            edges = list(g.edges())
            print(f"({len(edges)} edges)" if edges else "(no edges yet)")
            for u, v, w in edges:
                print(f"  {u} -> {v}   weight={w}")

        elif choice == "5":
            n = input("Number of nodes (default 8): ").strip()
            e = input("Number of edges (default 14): ").strip()
            n = int(n) if n else 8
            e = int(e) if e else 14
            neg = input("Allow negative weights? (y/N): ").strip().lower() == "y"
            new_g = random_graph(n, e, allow_negative=neg)
            g.adj = new_g.adj
            print(f"Loaded random graph: {n} nodes, {e} edges, negative_weights={neg}")

        elif choice == "6":
            g.adj = {}
            print("Graph cleared.")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Dijkstra sub-menu
def run_dijkstra_demo(g):
    print("\n--- Dijkstra: shortest path (non-negative weights) ---")
    while True:
        print(
            "\nDijkstra menu:\n"
            "  1) Run from a source node (show all distances)\n"
            "  2) Show shortest path to a specific target\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice in ("1", "2"):
            if not g.nodes():
                print("Graph is empty. Build a graph first.")
                continue
            source = input(f"Source node {g.nodes()}: ").strip()
            if source not in g.adj:
                print("That node isn't in the graph.")
                continue
            try:
                dist, prev, order = dijkstra(g, source)
            except ValueError as e:
                print(f"Error: {e}")
                continue

            if choice == "1":
                print(f"Visit order: {order}")
                for node, d in dist.items():
                    print(f"  {source} -> {node}: {d}")
            else:
                target = input(f"Target node {g.nodes()}: ").strip()
                if target not in g.adj:
                    print("That node isn't in the graph.")
                    continue
                if dist[target] == float('inf'):
                    print(f"No path from {source} to {target}.")
                else:
                    path = reconstruct_path(prev, target)
                    print(f"Shortest distance: {dist[target]}")
                    print(f"Path: {' -> '.join(path)}")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Prim sub-menu
def run_prim_demo(g):
    print("\n--- Prim: minimum spanning tree ---")
    while True:
        print(
            "\nPrim menu:\n"
            "  1) Build MST from a source node\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            if not g.nodes():
                print("Graph is empty. Build a graph first.")
                continue
            source = input(f"Source node {g.nodes()} (blank = auto-pick): ").strip()
            source = source if source else None
            if source is not None and source not in g.adj:
                print("That node isn't in the graph.")
                continue
            mst_edges, total = prim_mst(g, source)
            print(f"MST total weight: {total}")
            for u, v, w in mst_edges:
                print(f"  {u} -- {v}   weight={w}")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Bellman-Ford sub-menu
def run_bellman_ford_demo(g):
    print("\n--- Bellman-Ford: shortest path, handles negative weights ---")
    while True:
        print(
            "\nBellman-Ford menu:\n"
            "  1) Run from a source node (show all distances)\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            if not g.nodes():
                print("Graph is empty. Build a graph first.")
                continue
            source = input(f"Source node {g.nodes()}: ").strip()
            if source not in g.adj:
                print("That node isn't in the graph.")
                continue
            dist, prev, negative_cycle = bellman_ford(g, source)
            if negative_cycle:
                print("Negative-weight cycle detected — distances below are not reliable.")
            for node, d in dist.items():
                print(f"  {source} -> {node}: {d}")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Main menu loop
def main():
    g = Graph(directed=True)

    demos = {
        "1": ("Build / edit the graph", lambda: run_graph_builder(g)),
        "2": ("Run Dijkstra (shortest path)", lambda: run_dijkstra_demo(g)),
        "3": ("Run Prim (minimum spanning tree)", lambda: run_prim_demo(g)),
        "4": ("Run Bellman-Ford (negative weights)", lambda: run_bellman_ford_demo(g)),
    }

    while True:
        print("\n===== Task 2: Graph Algorithms =====")
        for key, (label, _) in demos.items():
            print(f"  {key}) {label}")
        print("  0) Exit")

        choice = input("What do you want to do? ").strip()

        if choice == "0":
            print("Goodbye.")
            break
        elif choice in demos:
            _, fn = demos[choice]
            fn()
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
