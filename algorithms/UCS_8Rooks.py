import heapq

def RookCost(state, col, solution):
    """Tính chi phí đặt quân vào cột col ở state hiện tại."""
    row = len(state)
    target_col = solution[row]
    dis = abs(col - target_col)
    cost = dis + 1
    return cost

def UniformCostSearch(solution, mode="all"):
    """UCS cho bài 8 Rooks với visited set và hỗ trợ mode='all'."""
    N = len(solution)
    start = ()
    Queue = [(0, start)]  # (cost, state)
    heapq.heapify(Queue)

    visited = set()
    visited.add(start)

    all_states = [] if mode == "all" else None

    while Queue:
        cost, col_select = heapq.heappop(Queue)

        if mode == "all":
            all_states.append(list(col_select))

        # Nếu đã đầy N quân
        if len(col_select) == N:
            if list(col_select) == solution:
                if mode == "all":
                    return all_states
                return list(col_select)
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

    return all_states if mode == "all" else []
