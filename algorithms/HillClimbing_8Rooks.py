def H_match(state, solution):
    """Số quân đặt đúng vị trí so với solution (càng nhiều càng tốt)"""
    return sum(1 for i in range(len(state)) if state[i] == solution[i])


def HillClimbing(solution):
    n = len(solution)
    current = []            
    path = [list(current)] 

    for row in range(n):
        # Sinh tất cả neighbor 
        candidates = []
        for col in range(n):
            if col not in current: 
                next_state = current + [col]
                h = H_match(next_state, solution)
                candidates.append((h, next_state))

        if not candidates:
            return None  # hết nước đi

        # chọn neighbor có h lớn nhất 
        best_h, best_state = max(candidates, key=lambda x: x[0])
        current_h = H_match(current, solution)

        # Nếu không tốt hơn thì dừng 
        if best_h <= current_h:
            return None

        current = best_state
        path.append(list(current))

        if current == list(solution):
            return path

    return None