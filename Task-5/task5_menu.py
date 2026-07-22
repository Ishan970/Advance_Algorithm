"""
Task 5: Interactive demo for sequential vs threaded vs multiprocessing merge sort.
"""

from algorithms5 import run_sequential, run_threaded, run_multiprocessing


def read_int(prompt, default=None):
    raw = input(prompt).strip()
    if not raw and default is not None:
        return default
    try:
        return int(raw)
    except ValueError:
        print("Please enter a valid whole number.")
        return None


# Sequential sub-menu
def run_sequential_demo(state):
    print("\n--- Sequential merge sort (baseline) ---")
    while True:
        print(
            "\nSequential menu:\n"
            "  1) Run sequential sort\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            n = read_int(f"Array size (default {state['n']}): ", state['n'])
            if n is None:
                continue
            state['n'] = n
            elapsed, _ = run_sequential(n)
            state['results']['sequential'] = elapsed
            print(f"Sorted {n} items in {elapsed*1000:.3f} ms")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Threaded sub-menu
def run_threaded_demo(state):
    print("\n--- Threaded parallel merge sort (threading.Thread) ---")
    while True:
        print(
            "\nThreaded menu:\n"
            "  1) Run with a given thread budget\n"
            "  2) Run a full sweep (1, 2, 4, 8 threads)\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            n = read_int(f"Array size (default {state['n']}): ", state['n'])
            if n is None:
                continue
            state['n'] = n
            budget = read_int("Thread budget (e.g. 1, 2, 4, 8): ")
            if budget is None:
                continue
            elapsed, _ = run_threaded(n, budget)
            state['results'][f'threaded_{budget}'] = elapsed
            print(f"Sorted {n} items with thread_budget={budget} in {elapsed*1000:.3f} ms")

        elif choice == "2":
            n = read_int(f"Array size (default {state['n']}): ", state['n'])
            if n is None:
                continue
            state['n'] = n
            print(f"Running sweep on {n} items...")
            for budget in (1, 2, 4, 8):
                elapsed, _ = run_threaded(n, budget)
                state['results'][f'threaded_{budget}'] = elapsed
                print(f"  threads={budget}: {elapsed*1000:.3f} ms")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Multiprocessing sub-menu
def run_multiprocessing_demo(state):
    print("\n--- Multiprocessing parallel sort (multiprocessing.Pool) ---")
    while True:
        print(
            "\nMultiprocessing menu:\n"
            "  1) Run with a given process count\n"
            "  2) Run a full sweep (1, 2, 4 processes)\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            n = read_int(f"Array size (default {state['n']}): ", state['n'])
            if n is None:
                continue
            state['n'] = n
            procs = read_int("Process count (e.g. 1, 2, 4): ")
            if procs is None:
                continue
            elapsed, _ = run_multiprocessing(n, procs)
            state['results'][f'mp_{procs}'] = elapsed
            print(f"Sorted {n} items with processes={procs} in {elapsed*1000:.3f} ms")

        elif choice == "2":
            n = read_int(f"Array size (default {state['n']}): ", state['n'])
            if n is None:
                continue
            state['n'] = n
            print(f"Running sweep on {n} items...")
            for procs in (1, 2, 4):
                elapsed, _ = run_multiprocessing(n, procs)
                state['results'][f'mp_{procs}'] = elapsed
                print(f"  processes={procs}: {elapsed*1000:.3f} ms")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Results / comparison sub-menu
def run_results_demo(state):
    print("\n--- Recorded results ---")
    if not state['results']:
        print("(no results yet - run some sorts first)")
        input("\nPress Enter to go back...")
        return

    baseline = state['results'].get('sequential')
    for label, elapsed in state['results'].items():
        line = f"  {label:16s}: {elapsed*1000:.3f} ms"
        if baseline and label != 'sequential':
            line += f"   (speedup vs sequential: {baseline/elapsed:.2f}x)"
        print(line)
    input("\nPress Enter to go back...")


# Main menu loop
def main():
    state = {"n": 200_000, "results": {}}

    demos = {
        "1": ("Sequential sort (baseline)", lambda: run_sequential_demo(state)),
        "2": ("Threaded parallel sort", lambda: run_threaded_demo(state)),
        "3": ("Multiprocessing parallel sort", lambda: run_multiprocessing_demo(state)),
        "4": ("Show recorded results / speedup", lambda: run_results_demo(state)),
    }

    while True:
        print("\n===== Task 5: Concurrent Programming =====")
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
