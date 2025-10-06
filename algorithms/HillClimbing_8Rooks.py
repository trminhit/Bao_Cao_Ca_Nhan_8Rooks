def H_match(state, solution):
    """Số quân đặt đúng vị trí so với solution (càng nhiều càng tốt)"""
    return sum(1 for i in range(len(state)) if state[i] == solution[i])

def HillClimbing(solution, mode="goal"):
    """
    Hill Climbing cho 8 Rooks
    """
    n = len(solution)
    current = []
    path = [list(current)] if mode == "all" else None

    for row in range(n):
        candidates = []
        for col in range(n):
            if col not in current:  # constraint: không trùng cột
                next_state = current + [col]
                h = H_match(next_state, solution)
                candidates.append((h, next_state))

        if not candidates:
            return None  # hết nước đi

        # chọn neighbor có h lớn nhất
        best_h, best_state = max(candidates, key=lambda x: x[0])
        current_h = H_match(current, solution)

        # nếu không cải thiện -> dừng
        if best_h <= current_h:
            return None

        current = best_state
        if mode == "all":
            path.append(list(current))  # lưu bước trung gian

        # kiểm tra đạt goal
        if current == list(solution):
            if mode == "all":
                return path
            else:  # mode "goal"
                return list(current)

    return None
