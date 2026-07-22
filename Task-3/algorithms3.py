"""
Task 3: Weighted Job Scheduling (DP), Minimum Platforms (Greedy),
Knight's Tour (Backtracking).
"""

from bisect import bisect_right


# Dynamic Programming: Weighted Job Scheduling
def weighted_job_scheduling(jobs):
    """jobs: list of (start, end, profit). Returns (max_profit, chosen_jobs)."""
    jobs = sorted(jobs, key=lambda j: j[1])
    n = len(jobs)
    ends = [j[1] for j in jobs]

    dp = [0] * (n + 1)
    choice = [False] * (n + 1)

    for i in range(1, n + 1):
        start_i, end_i, profit_i = jobs[i - 1]
        p = bisect_right(ends, start_i, 0, i - 1)
        include_profit = profit_i + dp[p]
        if include_profit > dp[i - 1]:
            dp[i] = include_profit
            choice[i] = True
        else:
            dp[i] = dp[i - 1]
            choice[i] = False

    chosen = []
    i = n
    while i > 0:
        if choice[i]:
            chosen.append(jobs[i - 1])
            start_i = jobs[i - 1][0]
            i = bisect_right(ends, start_i, 0, i - 1)
        else:
            i -= 1
    chosen.reverse()
    return dp[n], chosen


# Greedy: Minimum Number of Platforms
def min_platforms(arrivals, departures):
    arrivals = sorted(arrivals)
    departures = sorted(departures)
    n = len(arrivals)

    platforms_needed = 0
    max_platforms = 0
    i = j = 0

    while i < n and j < n:
        if arrivals[i] <= departures[j]:
            platforms_needed += 1
            max_platforms = max(max_platforms, platforms_needed)
            i += 1
        else:
            platforms_needed -= 1
            j += 1

    return max_platforms


def min_platforms_bruteforce(arrivals, departures):
    """O(n * T) exact check, used only to verify the greedy result."""
    n = len(arrivals)
    t_min, t_max = min(arrivals), max(departures)
    best = 0
    for t in range(t_min, t_max + 1):
        count = sum(1 for k in range(n) if arrivals[k] <= t <= departures[k])
        best = max(best, count)
    return best


# Backtracking: Knight's Tour with Warnsdorff pruning
MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def _degree(board, n, pos):
    x, y = pos
    count = 0
    for dx, dy in MOVES:
        nx_, ny_ = x + dx, y + dy
        if 0 <= nx_ < n and 0 <= ny_ < n and board[nx_][ny_] == -1:
            count += 1
    return count


def knights_tour(n, start=(0, 0)):
    board = [[-1] * n for _ in range(n)]
    board[start[0]][start[1]] = 0
    path = [start]

    def backtrack(pos, move_count):
        if move_count == n * n:
            return True
        x, y = pos
        candidates = []
        for dx, dy in MOVES:
            nx_, ny_ = x + dx, y + dy
            if 0 <= nx_ < n and 0 <= ny_ < n and board[nx_][ny_] == -1:
                candidates.append((nx_, ny_))

        candidates.sort(key=lambda p: _degree(board, n, p))  # Warnsdorff's rule

        for nxt in candidates:
            nx_, ny_ = nxt
            board[nx_][ny_] = move_count
            path.append(nxt)
            if backtrack(nxt, move_count + 1):
                return True
            board[nx_][ny_] = -1
            path.pop()
        return False

    success = backtrack(start, 1)
    return success, (board if success else None), (path if success else None)


def print_board(board):
    n = len(board)
    width = len(str(n * n))
    for row in board:
        print(' '.join(f"{v:>{width}d}" for v in row))
