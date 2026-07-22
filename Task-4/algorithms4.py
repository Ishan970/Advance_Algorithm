"""
Task 4: Multi-dimensional Bin Packing - Greedy (FFD) + Local Search heuristics.
"""

import random
import time
from dataclasses import dataclass, field


@dataclass
class Item:
    name: str
    demand: tuple  # (cpu, ram, bandwidth)


@dataclass
class Bin:
    capacity: tuple
    items: list = field(default_factory=list)

    def used(self):
        u = [0] * len(self.capacity)
        for it in self.items:
            for i, d in enumerate(it.demand):
                u[i] += d
        return tuple(u)

    def fits(self, item):
        used = self.used()
        return all(used[i] + item.demand[i] <= self.capacity[i] for i in range(len(self.capacity)))


def norm(vec):
    return sum(v * v for v in vec) ** 0.5


# Heuristic 1: Greedy construction - First-Fit Decreasing
def first_fit_decreasing(items, capacity):
    items_sorted = sorted(items, key=lambda it: norm(it.demand), reverse=True)
    bins = []
    for item in items_sorted:
        placed = False
        for b in bins:
            if b.fits(item):
                b.items.append(item)
                placed = True
                break
        if not placed:
            new_bin = Bin(capacity=capacity)
            new_bin.items.append(item)
            bins.append(new_bin)
    return bins


# Heuristic 2: Local search - relocate moves, only accept non-worsening ones
def local_search(bins, capacity, max_iters=2000, seed=0):
    rnd = random.Random(seed)
    bins = [Bin(capacity=capacity, items=list(b.items)) for b in bins]

    def objective(bins_):
        return len([b for b in bins_ if b.items])

    best_obj = objective(bins)

    for _ in range(max_iters):
        non_empty = [b for b in bins if b.items]
        if len(non_empty) <= 1:
            break
        b1, b2 = rnd.sample(non_empty, 2)
        if not b1.items:
            continue
        i1 = rnd.randrange(len(b1.items))
        item1 = b1.items[i1]

        b1.items.pop(i1)
        if b2.fits(item1):
            b2.items.append(item1)
        else:
            b1.items.insert(i1, item1)
            continue

        bins = [b for b in bins if b.items] + [Bin(capacity=capacity)]
        new_obj = objective(bins)
        if new_obj <= best_obj:
            best_obj = new_obj
        else:
            b2.items.remove(item1)
            b1.items.insert(i1, item1)

    return [b for b in bins if b.items]


def random_items(n, seed=1, lo=5, hi=40):
    rnd = random.Random(seed)
    return [Item(f"item{i}", (rnd.randint(lo, hi), rnd.randint(lo, hi), rnd.randint(lo, hi)))
            for i in range(n)]


def utilisation(bins, capacity):
    if not bins:
        return 0.0
    total_cap = len(bins) * sum(capacity)
    total_used = sum(sum(b.used()) for b in bins)
    return total_used / total_cap
