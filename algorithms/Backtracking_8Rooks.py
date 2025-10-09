import random
from engine.performance import PerformanceTracker

def Backtracking(solution, mode="all"):
    """
    Thuật toán Backtracking cho bài toán 8 Rooks.
    Variables: mỗi hàng là một biến (len(state) = hàng hiện tại)
    Domains: các cột khả thi (range(n)) sẽ được shuffle để random hóa
    Constraints: không có hai quân nào cùng cột
    """
    n = len(solution)
    all_states = [] if mode == "all" else None
    perf = PerformanceTracker("Backtracking")
    perf.start()
    
    def Backtrack(state):
        perf.add_node()  # tính mỗi state
        if mode == "all":
            all_states.append(state.copy())

        #nếu đã đặt đủ n quân
        if len(state) == n:
            if state == solution:
                perf.goal_found()
                return True
            else:
                return False

        # tạo danh sách cột khả thi cho hàng hiện tại
        candidates = list(range(n))
        random.shuffle(candidates)

        # thử từng cột trong candidates
        for col in candidates:
            if col not in state:
                state.append(col)
                result = Backtrack(state)
                if result and mode == "goal":
                    return True
                state.pop()

        return False

    Backtrack([])
    perf.stop()

    if mode == "all":
        return all_states, perf.get_stats()
    else:
        return solution, perf.get_stats()