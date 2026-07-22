"""
Task 4: Interactive demo for Multi-dimensional Bin Packing
(Greedy First-Fit-Decreasing + Local Search heuristics).
"""

import time
from algorithms4 import Item, first_fit_decreasing, local_search, random_items, utilisation


def read_int(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Please enter a valid whole number.")
        return None


def show_bins(bins, capacity):
    if not bins:
        print("(no bins yet - run a heuristic first)")
        return
    for i, b in enumerate(bins):
        used = b.used()
        names = ", ".join(it.name for it in b.items)
        print(f"  Bin {i}: used={used} / capacity={capacity}   items=[{names}]")


# Item manager sub-menu
def run_item_manager(state):
    print("\n--- Item manager ---")
    while True:
        print(
            "\nItem menu:\n"
            "  1) Add an item (cpu, ram, bandwidth)\n"
            "  2) Show all items\n"
            "  3) Load random sample items\n"
            "  4) Set bin capacity (cpu, ram, bandwidth)\n"
            "  5) Show current bin capacity\n"
            "  6) Clear items\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            cpu = read_int("CPU demand: ")
            if cpu is None:
                continue
            ram = read_int("RAM demand: ")
            if ram is None:
                continue
            bw = read_int("Bandwidth demand: ")
            if bw is None:
                continue
            name = f"item{len(state['items'])}"
            state["items"].append(Item(name, (cpu, ram, bw)))
            print(f"Added {name}: demand=({cpu}, {ram}, {bw})")

        elif choice == "2":
            if not state["items"]:
                print("(no items yet)")
            for it in state["items"]:
                print(f"  {it.name}: demand={it.demand}")

        elif choice == "3":
            n = read_int("How many random items (default 30): ") or 30
            state["items"] = random_items(n, seed=1)
            print(f"Loaded {n} random items.")

        elif choice == "4":
            cpu = read_int("Bin CPU capacity: ")
            if cpu is None:
                continue
            ram = read_int("Bin RAM capacity: ")
            if ram is None:
                continue
            bw = read_int("Bin bandwidth capacity: ")
            if bw is None:
                continue
            state["capacity"] = (cpu, ram, bw)
            print(f"Bin capacity set to {state['capacity']}")

        elif choice == "5":
            print(f"Current bin capacity: {state['capacity']}")

        elif choice == "6":
            state["items"] = []
            print("Items cleared.")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Greedy (FFD) sub-menu
def run_greedy_demo(state):
    print("\n--- Greedy: First-Fit Decreasing ---")
    while True:
        print(
            "\nGreedy menu:\n"
            "  1) Run FFD on current items\n"
            "  2) Show last FFD result\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            if not state["items"]:
                print("No items yet. Add some in the item manager first.")
                continue
            t0 = time.perf_counter()
            bins = first_fit_decreasing(state["items"], state["capacity"])
            elapsed = time.perf_counter() - t0
            state["ffd_bins"] = bins
            print(f"FFD used {len(bins)} bins in {elapsed*1000:.3f} ms")
            print(f"Average utilisation: {utilisation(bins, state['capacity'])*100:.1f}%")

        elif choice == "2":
            show_bins(state["ffd_bins"], state["capacity"])

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Local search sub-menu
def run_local_search_demo(state):
    print("\n--- Local Search (improves on the FFD result) ---")
    while True:
        print(
            "\nLocal search menu:\n"
            "  1) Run local search (starts from last FFD result)\n"
            "  2) Show last local search result\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            if not state["ffd_bins"]:
                print("Run Greedy (FFD) first — local search improves on that result.")
                continue
            iters = read_int("Max iterations (default 2000): ") or 2000
            t0 = time.perf_counter()
            bins = local_search(state["ffd_bins"], state["capacity"], max_iters=iters)
            elapsed = time.perf_counter() - t0
            state["ls_bins"] = bins
            print(f"Local search used {len(bins)} bins in {elapsed*1000:.3f} ms"
                  f" (started from {len(state['ffd_bins'])} bins)")
            print(f"Average utilisation: {utilisation(bins, state['capacity'])*100:.1f}%")

        elif choice == "2":
            show_bins(state["ls_bins"], state["capacity"])

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Comparison sub-menu
def run_comparison(state):
    print("\n--- Compare Greedy vs Local Search ---")
    if not state["ffd_bins"]:
        print("Run Greedy (FFD) first.")
        return
    if not state["ls_bins"]:
        print("Run Local Search first.")
        return

    ffd_n = len(state["ffd_bins"])
    ls_n = len(state["ls_bins"])
    ffd_u = utilisation(state["ffd_bins"], state["capacity"]) * 100
    ls_u = utilisation(state["ls_bins"], state["capacity"]) * 100

    print(f"Greedy (FFD):   {ffd_n} bins   utilisation={ffd_u:.1f}%")
    print(f"Local search:   {ls_n} bins   utilisation={ls_u:.1f}%")
    if ls_n < ffd_n:
        print(f"Local search improved on FFD by {ffd_n - ls_n} bin(s).")
    elif ls_n == ffd_n:
        print("Local search did not reduce the bin count on this instance.")
    else:
        print("Unexpected: local search used more bins than FFD.")
    input("\nPress Enter to go back...")


# Main menu loop
def main():
    state = {
        "items": [],
        "capacity": (100, 100, 100),
        "ffd_bins": [],
        "ls_bins": [],
    }

    demos = {
        "1": ("Manage items / bin capacity", lambda: run_item_manager(state)),
        "2": ("Run Greedy (First-Fit Decreasing)", lambda: run_greedy_demo(state)),
        "3": ("Run Local Search (improve FFD result)", lambda: run_local_search_demo(state)),
        "4": ("Compare Greedy vs Local Search", lambda: run_comparison(state)),
    }

    while True:
        print("\n===== Task 4: NP-Hard Problem - Bin Packing =====")
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
