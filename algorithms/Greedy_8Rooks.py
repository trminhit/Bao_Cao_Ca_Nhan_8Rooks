import heapq

def H_Manhattan(state, solution):
    """Tính tổng khoảng cách Manhattan giữa state và solution"""
    return sum(abs(state[i] - solution[i]) for i in range(len(state)))

def GreedySearch(solution=None, mode="goal"):
    """
    - Mỗi state là tuple các cột đã đặt.
    - Dùng H_Manhattan làm heuristic.
    - Thêm quân đưa vào queue.
    - Luôn mở node có h nhỏ nhất (gần Goal nhất).
    """
    N = 8
    start = ()
    Queue = [(H_Manhattan(start, solution), start)]
    heapq.heapify(Queue)
    all_states = [] if mode == "all" else None

    while Queue:
        h, state = heapq.heappop(Queue)

        # Lưu bước trung gian nếu mode "all"
        if mode == "all":
            all_states.append(list(state))

        if len(state) == N:
            if list(state) == solution:
                if mode == "all":
                    return all_states  # trả tất cả bước đến solution
                return list(state)  # mode goal
            else:
                continue

        row = len(state)
        for col in range(N):
            if col not in state:  
                new_state = state + (col,)
                new_h = H_Manhattan(new_state, solution)
                heapq.heappush(Queue, (new_h, new_state))
    # Nếu không tìm được solution
    if mode == "all":
        return all_states
    return None
