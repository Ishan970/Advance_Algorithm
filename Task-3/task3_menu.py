"""
Task 3: Interactive demo for Weighted Job Scheduling (DP),
Minimum Platforms (Greedy), Knight's Tour (Backtracking).
"""

from algorithms3 import (
    weighted_job_scheduling,
    min_platforms,
    min_platforms_bruteforce,
    knights_tour,
    print_board,
)


def read_int(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Please enter a valid whole number.")
        return None


# DP sub-menu
def run_dp_demo(jobs):
    print("\n--- Weighted Job Scheduling (Dynamic Programming) ---")
    while True:
        print(
            "\nDP menu:\n"
            "  1) Add a job (start, end, profit)\n"
            "  2) Show all jobs\n"
            "  3) Load sample job list\n"
            "  4) Clear jobs\n"
            "  5) Run scheduler (find max profit)\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            s = read_int("Start time: ")
            if s is None:
                continue
            e = read_int("End time: ")
            if e is None:
                continue
            p = read_int("Profit: ")
            if p is None:
                continue
            jobs.append((s, e, p))
            print(f"Added job (start={s}, end={e}, profit={p})")

        elif choice == "2":
            if not jobs:
                print("(no jobs yet)")
            for i, j in enumerate(jobs):
                print(f"  [{i}] start={j[0]} end={j[1]} profit={j[2]}")

        elif choice == "3":
            jobs.clear()
            jobs.extend([(1, 3, 5), (2, 5, 6), (4, 6, 5), (6, 7, 4), (5, 8, 11), (7, 9, 2)])
            print("Loaded 6 sample jobs.")

        elif choice == "4":
            jobs.clear()
            print("Jobs cleared.")

        elif choice == "5":
            if not jobs:
                print("No jobs to schedule. Add some first.")
                continue
            profit, chosen = weighted_job_scheduling(jobs)
            print(f"Max profit: {profit}")
            print("Chosen jobs:")
            for s, e, p in chosen:
                print(f"  start={s} end={e} profit={p}")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Greedy sub-menu
def run_greedy_demo(trains):
    print("\n--- Minimum Number of Platforms (Greedy) ---")
    while True:
        print(
            "\nGreedy menu:\n"
            "  1) Add a train (arrival, departure)\n"
            "  2) Show all trains\n"
            "  3) Load sample timetable\n"
            "  4) Clear trains\n"
            "  5) Compute minimum platforms needed\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            a = read_int("Arrival time (e.g. 900 for 9:00): ")
            if a is None:
                continue
            d = read_int("Departure time: ")
            if d is None:
                continue
            trains.append((a, d))
            print(f"Added train (arrival={a}, departure={d})")

        elif choice == "2":
            if not trains:
                print("(no trains yet)")
            for i, (a, d) in enumerate(trains):
                print(f"  [{i}] arrival={a} departure={d}")

        elif choice == "3":
            trains.clear()
            trains.extend([(900, 910), (940, 1200), (950, 1120), (1100, 1130), (1500, 1900), (1800, 2000)])
            print("Loaded 6 sample trains.")

        elif choice == "4":
            trains.clear()
            print("Trains cleared.")

        elif choice == "5":
            if not trains:
                print("No trains yet. Add some first.")
                continue
            arrivals = [a for a, _ in trains]
            departures = [d for _, d in trains]
            result = min_platforms(arrivals, departures)
            print(f"Minimum platforms needed: {result}")
            if len(trains) <= 20:
                check = min_platforms_bruteforce(arrivals, departures)
                match = "matches" if check == result else "MISMATCH with"
                print(f"Brute-force check: {check}  ({match} greedy result)")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Backtracking sub-menu
def run_backtracking_demo():
    print("\n--- Knight's Tour (Backtracking + Warnsdorff pruning) ---")
    while True:
        print(
            "\nBacktracking menu:\n"
            "  1) Run a tour on an n x n board\n"
            "  0) Back to main menu"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            n = read_int("Board size n (e.g. 5, 6, 8): ")
            if n is None or n < 5:
                print("Pick n >= 5.")
                continue
            sx = read_int("Start row (0-indexed, default 0): ") or 0
            sy = read_int("Start col (0-indexed, default 0): ") or 0
            if not (0 <= sx < n and 0 <= sy < n):
                print("Start position out of bounds.")
                continue
            success, board, path = knights_tour(n, start=(sx, sy))
            if success:
                print(f"Tour found! Move order shown as move numbers (0 = start):")
                print_board(board)
            else:
                print("No tour found from that starting square.")

        elif choice == "0":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, try again.")


# Main menu loop
def main():
    jobs = []
    trains = []

    demos = {
        "1": ("Weighted Job Scheduling (DP)", lambda: run_dp_demo(jobs)),
        "2": ("Minimum Platforms (Greedy)", lambda: run_greedy_demo(trains)),
        "3": ("Knight's Tour (Backtracking)", run_backtracking_demo),
    }

    while True:
        print("\n===== Task 3: Algorithmic Strategies =====")
        for key, (label, _) in demos.items():
            print(f"  {key}) {label}")
        print("  0) Exit")

        choice = input("What do you want to try? ").strip()

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
