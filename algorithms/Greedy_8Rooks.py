import heapq

def H_Manhattan(state, solution):
    """Tính tổng khoảng cách Manhattan giữa state và solution"""
    return sum(abs(state[i] - solution[i]) for i in range(len(state)))

def GreedySearch(solution):
    """
    - Mỗi state là tuple các cột đã đặt.
    - Dùng H_Manhattan làm heuristic.
    - Thêm quân đưa vào queue.
    - Luôn mở node có h nhỏ nhất (gần Goal nhất).
    """
    N = len(solution)
    start = ()
    Queue = [(H_Manhattan(start, solution), start)]
    heapq.heapify(Queue)
    expanded_nodes = 0

    while Queue:
        h, state = heapq.heappop(Queue)
        if len(state) == N:
            if list(state) == solution:
                return list(state)
            else:
                continue

        row = len(state)
        for col in range(N):
            if col not in state:
                new_state = state + (col,)
                new_h = H_Manhattan(new_state, solution)
                heapq.heappush(Queue, (new_h, new_state))
    return None
