def Backtracking_8Rooks(n=8, goal=None, mode="all"):
    """
    Backtracking cơ bản cho bài toán đặt n quân xe.
    - mode = "all": trả về tất cả state đi qua (dùng cho animation)
    - mode = "goal": trả về state cuối cùng đầy đủ n quân (hoặc goal nếu có)
    """
    goal_list = list(goal) if goal is not None else None
    all_states = []

    def backtrack(state):
        if state:
            all_states.append(state[:])  # Lưu state hiện tại

        # Kiểm tra solution / goal
        if len(state) == n:
            if goal_list is not None:
                if state == goal_list:
                    return state
                else:
                    return None
            else:
                return state

        for col in range(n):
            if col not in state:  # Ràng buộc cột
                result = backtrack(state + [col])
                if result is not None and mode == "goal":
                    return result

        return None

    result = backtrack([])

    return all_states if mode == "all" else result
