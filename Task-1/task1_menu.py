"""
Task 1: Interactive demo for BST, AVL Tree, Min-Heap, Hash Table.
"""

import random
from structures import City, BST, AVLTree, MinHeap, HashTable


def random_city(i=None, rnd=None):
    rnd = rnd or random
    i = i if i is not None else rnd.randint(0, 9999)
    return City(
        name=f"City{i}",
        x=round(rnd.uniform(0, 1000), 1),
        y=round(rnd.uniform(0, 1000), 1),
        population=rnd.randint(1000, 2_000_000),
        distance=round(rnd.uniform(0, 1000), 1),
    )


def read_float(prompt):
    try:
        return float(input(prompt).strip())
    except ValueError:
        print("Please enter a valid number.")
        return None


# BST sub-menu
def run_bst_demo(bst):
    print("\n--- Binary Search Tree demo ---")
    while True:
        print(
            "\nBST menu:\n"
            "  1) Insert a random city\n"
            "  2) Insert a city with a specific distance\n"
            "  3) Search by distance\n"
            "  4) Delete by distance\n"
            "  5) Show all cities (sorted by distance)\n"
            "  6) Show tree stats (size, height)\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            c = random_city()
            bst.insert(c.distance, c)
            print(f"Inserted: {c}")

        elif choice == "2":
            dist = read_float("Distance value (key): ")
            if dist is None:
                continue
            name = input("City name: ").strip() or f"City{dist}"
            c = City(name, 0, 0, 0, dist)
            bst.insert(dist, c)
            print(f"Inserted: {c}")

        elif choice == "3":
            dist = read_float("Distance to search for: ")
            if dist is None:
                continue
            result = bst.search(dist)
            print(f"Found: {result}" if result else "Not found.")

        elif choice == "4":
            dist = read_float("Distance to delete: ")
            if dist is None:
                continue
            if bst.search(dist) is None:
                print("That key isn't in the tree.")
            else:
                bst.delete(dist)
                print(f"Deleted city with distance={dist}.")

        elif choice == "5":
            entries = bst.inorder()
            if not entries:
                print("(tree is empty)")
            else:
                for key, city in entries:
                    print(f"  {city}")

        elif choice == "6":
            print(f"Size: {bst.size}   Height: {bst.height()}")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# AVL sub-menu
def run_avl_demo(avl):
    print("\n--- AVL Tree demo (self-balancing) ---")
    while True:
        print(
            "\nAVL menu:\n"
            "  1) Insert a random city\n"
            "  2) Insert a city with a specific distance\n"
            "  3) Search by distance\n"
            "  4) Delete by distance\n"
            "  5) Show all cities (sorted by distance)\n"
            "  6) Show tree stats (size, height)\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            c = random_city()
            avl.insert(c.distance, c)
            print(f"Inserted: {c}   (height now {avl.height()})")

        elif choice == "2":
            dist = read_float("Distance value (key): ")
            if dist is None:
                continue
            name = input("City name: ").strip() or f"City{dist}"
            c = City(name, 0, 0, 0, dist)
            avl.insert(dist, c)
            print(f"Inserted: {c}   (height now {avl.height()})")

        elif choice == "3":
            dist = read_float("Distance to search for: ")
            if dist is None:
                continue
            result = avl.search(dist)
            print(f"Found: {result}" if result else "Not found.")

        elif choice == "4":
            dist = read_float("Distance to delete: ")
            if dist is None:
                continue
            if avl.search(dist) is None:
                print("That key isn't in the tree.")
            else:
                avl.delete(dist)
                print(f"Deleted city with distance={dist}.   (height now {avl.height()})")

        elif choice == "5":
            entries = avl.inorder()
            if not entries:
                print("(tree is empty)")
            else:
                for key, city in entries:
                    print(f"  {city}")

        elif choice == "6":
            print(f"Size: {avl.size}   Height: {avl.height()}")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Min-Heap sub-menu
def run_heap_demo(heap):
    print("\n--- Min-Heap demo (priority queue: nearest city first) ---")
    while True:
        print(
            "\nMin-Heap menu:\n"
            "  1) Push a random city\n"
            "  2) Push a city with a specific distance\n"
            "  3) Peek at the nearest city (no removal)\n"
            "  4) Pop the nearest city (removes it)\n"
            "  5) Show heap contents (heap order, not sorted)\n"
            "  6) Show stats (size)\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            c = random_city()
            heap.push(c.distance, c)
            print(f"Pushed: {c}")

        elif choice == "2":
            dist = read_float("Distance value (priority): ")
            if dist is None:
                continue
            name = input("City name: ").strip() or f"City{dist}"
            c = City(name, 0, 0, 0, dist)
            heap.push(dist, c)
            print(f"Pushed: {c}")

        elif choice == "3":
            top = heap.peek()
            print(f"Nearest: {top[1]}" if top else "(heap is empty)")

        elif choice == "4":
            if len(heap) == 0:
                print("(heap is empty)")
            else:
                _, city = heap.pop()
                print(f"Popped (was nearest): {city}")

        elif choice == "5":
            items = heap.as_list()
            if not items:
                print("(heap is empty)")
            else:
                for priority, city in items:
                    print(f"  {city}")

        elif choice == "6":
            print(f"Size: {len(heap)}")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Hash Table sub-menu
def run_hash_demo(ht):
    print("\n--- Hash Table demo (separate chaining, keyed on city name) ---")
    while True:
        print(
            "\nHash Table menu:\n"
            "  1) Insert a random city\n"
            "  2) Insert a city with a specific name\n"
            "  3) Search by name\n"
            "  4) Delete by name\n"
            "  5) Show all buckets (reveals collisions)\n"
            "  6) Show stats (size, capacity, load factor)\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            c = random_city()
            ht.insert(c.name, c)
            print(f"Inserted: {c}")

        elif choice == "2":
            name = input("City name (key): ").strip()
            if not name:
                print("Name can't be empty.")
                continue
            dist = read_float("Distance: ")
            if dist is None:
                continue
            c = City(name, 0, 0, 0, dist)
            ht.insert(name, c)
            print(f"Inserted: {c}")

        elif choice == "3":
            name = input("Name to search for: ").strip()
            result = ht.search(name)
            print(f"Found: {result}" if result else "Not found.")

        elif choice == "4":
            name = input("Name to delete: ").strip()
            if ht.delete(name):
                print(f"Deleted '{name}'.")
            else:
                print("That name isn't in the table.")

        elif choice == "5":
            snapshot = ht.bucket_snapshot()
            if not snapshot:
                print("(table is empty)")
            else:
                for idx, bucket in snapshot:
                    entries = ", ".join(str(city) for _, city in bucket)
                    tag = "  <- collision (chain > 1)" if len(bucket) > 1 else ""
                    print(f"  bucket[{idx}]: {entries}{tag}")

        elif choice == "6":
            print(f"Size: {ht.size}   Capacity: {ht.capacity}"
                  f"   Load factor: {ht.load_factor():.2f}")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Main menu loop
def main():
    bst = BST()
    avl = AVLTree()
    heap = MinHeap()
    ht = HashTable()

    demos = {
        "1": ("Binary Search Tree (BST)", lambda: run_bst_demo(bst)),
        "2": ("AVL Tree", lambda: run_avl_demo(avl)),
        "3": ("Min-Heap", lambda: run_heap_demo(heap)),
        "4": ("Hash Table", lambda: run_hash_demo(ht)),
    }

    while True:
        print("\n===== Task 1: Advanced Data Structures =====")
        for key, (label, _) in demos.items():
            print(f"  {key}) {label}")
        print("  0) Exit")

        choice = input("Which structure do you want to try? ").strip()

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
