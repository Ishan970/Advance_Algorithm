"""
Task 1: City data model + BST, AVL Tree, Min-Heap, Hash Table.
"""


class City:
    """A city record stored in every structure below."""
    __slots__ = ("name", "x", "y", "population", "distance")

    def __init__(self, name, x, y, population, distance):
        self.name = name
        self.x = x
        self.y = y
        self.population = population
        self.distance = distance

    def __repr__(self):
        return f"City({self.name}, dist={self.distance:.1f}, pop={self.population})"


# Binary Search Tree, keyed on distance
class BSTNode:
    __slots__ = ("key", "city", "left", "right")

    def __init__(self, key, city):
        self.key = key
        self.city = city
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, key, city):
        self.size += 1
        if self.root is None:
            self.root = BSTNode(key, city)
            return
        node = self.root
        while True:
            if key < node.key:
                if node.left is None:
                    node.left = BSTNode(key, city)
                    return
                node = node.left
            elif key > node.key:
                if node.right is None:
                    node.right = BSTNode(key, city)
                    return
                node = node.right
            else:  # duplicate key, chain to the right
                if node.right is None:
                    node.right = BSTNode(key, city)
                    return
                node = node.right

    def search(self, key):
        node = self.root
        while node is not None:
            if key == node.key:
                return node.city
            node = node.left if key < node.key else node.right
        return None

    def _min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            self.size -= 1
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = self._min_node(node.right)
            node.key, node.city = successor.key, successor.city
            node.right = self._delete(node.right, successor.key)
            self.size += 1  # undo the double decrement above
        return node

    def inorder(self):
        """(key, city) pairs sorted by key."""
        result = []

        def _walk(node):
            if node is None:
                return
            _walk(node.left)
            result.append((node.key, node.city))
            _walk(node.right)

        _walk(self.root)
        return result

    def height(self):
        def _h(node):
            if node is None:
                return 0
            return 1 + max(_h(node.left), _h(node.right))
        return _h(self.root)


# AVL Tree, self-balancing, keyed on distance
class AVLNode:
    __slots__ = ("key", "city", "left", "right", "height")

    def __init__(self, key, city):
        self.key = key
        self.city = city
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None
        self.size = 0

    @staticmethod
    def _h(node):
        return node.height if node else 0

    def _update(self, node):
        node.height = 1 + max(self._h(node.left), self._h(node.right))

    def _balance_factor(self, node):
        return self._h(node.left) - self._h(node.right)

    def _rotate_right(self, y):
        x = y.left
        t2 = x.right
        x.right = y
        y.left = t2
        self._update(y)
        self._update(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        t2 = y.left
        y.left = x
        x.right = t2
        self._update(x)
        self._update(y)
        return y

    def insert(self, key, city):
        self.size += 1
        self.root = self._insert(self.root, key, city)

    def _insert(self, node, key, city):
        if node is None:
            return AVLNode(key, city)
        if key < node.key:
            node.left = self._insert(node.left, key, city)
        else:
            node.right = self._insert(node.right, key, city)

        self._update(node)
        balance = self._balance_factor(node)

        if balance > 1 and key < node.left.key:          # Left-Left
            return self._rotate_right(node)
        if balance < -1 and key >= node.right.key:        # Right-Right
            return self._rotate_left(node)
        if balance > 1 and key >= node.left.key:           # Left-Right
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and key < node.right.key:          # Right-Left
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def search(self, key):
        node = self.root
        while node is not None:
            if key == node.key:
                return node.city
            node = node.left if key < node.key else node.right
        return None

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            self.size -= 1
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = self._min_node(node.right)
            node.key, node.city = successor.key, successor.city
            node.right = self._delete(node.right, successor.key)
            self.size += 1

        if node is None:
            return node
        self._update(node)
        balance = self._balance_factor(node)

        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)
        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)
        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def inorder(self):
        result = []

        def _walk(node):
            if node is None:
                return
            _walk(node.left)
            result.append((node.key, node.city))
            _walk(node.right)

        _walk(self.root)
        return result

    def height(self):
        return self._h(self.root)


# Min-Heap, array-based, priority queue for "nearest city"
class MinHeap:
    def __init__(self):
        self.heap = []  # list of (priority, city)

    def push(self, priority, city):
        self.heap.append((priority, city))
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            raise IndexError("pop from empty heap")
        top = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return top

    def peek(self):
        return self.heap[0] if self.heap else None

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i][0] < self.heap[parent][0]:
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self.heap)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i
            if left < n and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < n and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right
            if smallest == i:
                break
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            i = smallest

    def as_list(self):
        """Raw heap array, not sorted order."""
        return list(self.heap)

    def __len__(self):
        return len(self.heap)


# Hash Table, separate chaining, keyed on city name
class HashTable:
    def __init__(self, capacity=16, max_load_factor=0.75):
        self.capacity = capacity
        self.max_load_factor = max_load_factor
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0

    def _hash(self, key):
        return hash(key) % self.capacity

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        old_size = self.size
        self.size = 0
        for bucket in old_buckets:
            for k, v in bucket:
                self.insert(k, v)
        self.size = old_size

    def insert(self, key, city):
        if self.size / self.capacity >= self.max_load_factor:
            self._resize()
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, city)
                return
        bucket.append((key, city))
        self.size += 1

    def search(self, key):
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return None

    def delete(self, key):
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def load_factor(self):
        return self.size / self.capacity

    def bucket_snapshot(self):
        """Non-empty buckets as (index, [(key, city), ...])."""
        return [(i, b) for i, b in enumerate(self.buckets) if b]
