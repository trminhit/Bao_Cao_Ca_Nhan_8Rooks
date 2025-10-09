from .UCS_8Rooks import RookCost
from .Greedy_8Rooks import H_Manhattan
import heapq
from engine.performance import PerformanceTracker
from engine.common_goal import check_goal

def AStarSearch(solution=None, mode="goal"):
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

    all_states = [] if mode == "all" else None
    tracker = PerformanceTracker("A*")
    tracker.start()

    while Queue:
        f, g, state = heapq.heappop(Queue)
        tracker.add_node()

        # Lưu bước trung gian nếu mode "all"
        if mode == "all":
            all_states.append(list(state))

        # Kiểm tra goal
        if len(state) == N:
            if list(state) == solution:
                tracker.goal_found()
                tracker.stop()
                return (all_states, tracker.get_stats()) if mode=="all" else (list(state), tracker.get_stats())
            else:
                continue

        row = len(state)
        for col in range(N):
            if col not in state:
                new_state = state + (col,)
                new_g = g + RookCost(state, col, solution)
                new_h = H_Manhattan(new_state, solution)
                heapq.heappush(Queue, (new_g + new_h, new_g, new_state))

    tracker.stop()
    return (all_states, tracker.get_stats()) if mode=="all" else ([], tracker.get_stats())