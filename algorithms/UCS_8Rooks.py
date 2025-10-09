import heapq
from engine.performance import PerformanceTracker
from engine.common_goal import check_goal, handle_goal_found

def RookCost(state, col, solution):
    """Tính chi phí đặt quân vào cột col ở state hiện tại."""
    row = len(state)
    target_col = solution[row]
    dis = abs(col - target_col)
    cost = dis + 1
    return cost

def UniformCostSearch(solution, mode="all"):
    """UCS cho bài 8 Rooks"""
    N = len(solution)
    start = ()
    Queue = [(0, start)]  # (cost, state)
    heapq.heapify(Queue)

    visited = set()
    visited.add(start)

    all_states = [] if mode == "all" else None
    tracker = PerformanceTracker("UCS")
    tracker.start()

    while Queue:
        cost, col_select = heapq.heappop(Queue)
        tracker.add_node()

        if mode == "all":
            all_states.append(list(col_select))

        # Nếu đã đầy N quân
        if len(col_select) == N:
            if list(col_select) == solution:
                tracker.goal_found()
                tracker.stop()
                return (all_states, tracker.get_stats()) if mode=="all" else (list(col_select), tracker.get_stats())
            else:
                continue

        # Sinh các state con
        for col in range(N):
            if col not in col_select:
                new_state = col_select + (col,)
                if new_state not in visited:
                    new_cost = cost + RookCost(col_select, col, solution)
                    heapq.heappush(Queue, (new_cost, new_state))
                    visited.add(new_state)

    tracker.stop()
    return (all_states, tracker.get_stats()) if mode=="all" else ([], tracker.get_stats())