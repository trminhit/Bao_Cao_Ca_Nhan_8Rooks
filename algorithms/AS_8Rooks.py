from .UCS_8Rooks import RookCost
from .Greedy_8Rooks import H_Manhattan

import heapq

def AStarSearch(solution):
    """
    - Mỗi state là tuple các cột đã đặt.
    - Dùng f(n) = g(n) + h(n):
        + g(n): chi phí tích lũy (RookCost)
        + h(n): heuristic H_Manhattan (ước lượng khoảng cách tới goal)
    - Thêm node vào priority queue theo f(n) nhỏ nhất.
    """
    N = len(solution)
    start = ()
    Queue = [(H_Manhattan(start, solution), 0, start)]  # (f, g, state)
    heapq.heapify(Queue)

    while Queue:
        f, g, state = heapq.heappop(Queue)

        if len(state) == N:
            if list(state) == solution:
                return list(state)
            else:
                continue

        row = len(state)
        for col in range(N):
            if col not in state:
                new_state = state + (col,)
                new_g = g + RookCost(state, col, solution)
                new_h = H_Manhattan(new_state, solution)
                heapq.heappush(Queue, (new_g + new_h, new_g, new_state))

    return None