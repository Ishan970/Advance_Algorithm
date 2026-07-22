"""
Task 2: Graph representation + Dijkstra, Prim, Bellman-Ford.
"""

import heapq
import random


class Graph:
    """Weighted directed graph, adjacency list."""

    def __init__(self, directed=True):
        self.directed = directed
        self.adj = {}

    def add_node(self, u):
        self.adj.setdefault(u, [])

    def add_edge(self, u, v, w):
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append((v, w))
        if not self.directed:
            self.adj[v].append((u, w))

    def remove_edge(self, u, v):
        if u in self.adj:
            self.adj[u] = [(n, w) for n, w in self.adj[u] if n != v]
            if not self.directed and v in self.adj:
                self.adj[v] = [(n, w) for n, w in self.adj[v] if n != u]

    def nodes(self):
        return list(self.adj.keys())

    def edges(self):
        for u in self.adj:
            for v, w in self.adj[u]:
                yield (u, v, w)

    def has_negative_edge(self):
        return any(w < 0 for _, _, w in self.edges())


def dijkstra(graph, source):
    """Shortest paths from source. Requires non-negative weights."""
    dist = {v: float('inf') for v in graph.nodes()}
    prev = {v: None for v in graph.nodes()}
    dist[source] = 0
    pq = [(0, source)]
    visited = set()
    order = []

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        order.append(u)
        for v, w in graph.adj[u]:
            if w < 0:
                raise ValueError("Dijkstra cannot handle negative edge weights")
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev, order


def reconstruct_path(prev, target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    return list(reversed(path))


def prim_mst(graph, source=None):
    """Minimum spanning tree, treats the graph as undirected."""
    undirected_adj = {v: [] for v in graph.nodes()}
    for u, v, w in graph.edges():
        undirected_adj[u].append((v, w))
        undirected_adj[v].append((u, w))

    nodes = list(undirected_adj.keys())
    if not nodes:
        return [], 0
    source = source or nodes[0]

    visited = {source}
    edges_heap = [(w, source, v) for v, w in undirected_adj[source]]
    heapq.heapify(edges_heap)
    mst_edges = []
    total_weight = 0

    while edges_heap and len(visited) < len(nodes):
        w, u, v = heapq.heappop(edges_heap)
        if v in visited:
            continue
        visited.add(v)
        mst_edges.append((u, v, w))
        total_weight += w
        for nxt, nw in undirected_adj[v]:
            if nxt not in visited:
                heapq.heappush(edges_heap, (nw, v, nxt))

    return mst_edges, total_weight


def bellman_ford(graph, source):
    """Shortest paths, handles negative weights, flags negative cycles."""
    dist = {v: float('inf') for v in graph.nodes()}
    prev = {v: None for v in graph.nodes()}
    dist[source] = 0
    edge_list = list(graph.edges())

    for _ in range(len(graph.nodes()) - 1):
        updated = False
        for u, v, w in edge_list:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                updated = True
        if not updated:
            break

    negative_cycle = False
    for u, v, w in edge_list:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            negative_cycle = True
            break

    return dist, prev, negative_cycle


def random_graph(n_nodes, n_edges, seed=0, allow_negative=False, directed=True):
    """Connected random graph for quick testing/demos."""
    rnd = random.Random(seed)
    g = Graph(directed=directed)
    nodes = [f"N{i}" for i in range(n_nodes)]
    for n in nodes:
        g.add_node(n)
    shuffled = nodes[:]
    rnd.shuffle(shuffled)
    for i in range(len(shuffled) - 1):
        g.add_edge(shuffled[i], shuffled[i + 1], rnd.randint(1, 20))
    edges_added = len(shuffled) - 1
    while edges_added < n_edges:
        u, v = rnd.choice(nodes), rnd.choice(nodes)
        if u == v:
            continue
        w = rnd.randint(-5, 20) if allow_negative else rnd.randint(1, 20)
        g.add_edge(u, v, w)
        edges_added += 1
    return g
