import random, math

def H_match(state, solution):
    """Số quân đặt đúng vị trí so với solution (càng nhiều càng tốt)."""
    return sum(1 for i in range(len(state)) if state[i] == solution[i])

def SimulatedAnnealing(solution, T0, alpha):
    n = len(solution)
    current = []            
    path = [list(current)]
    T = T0

    for row in range(n):
        # Sinh tất cả neighbor
        candidates = []
        for col in range(n):
            if col not in current: 
                next_state = current + [col]
                h = H_match(next_state, solution)
                candidates.append((h, next_state))

        if not candidates:
            return None

        current_h = H_match(current, solution)

        # Tìm neighbor tốt nhất
        best_h, best_state = max(candidates, key=lambda x: x[0])

        if best_h > current_h:
            # Có tốt hơn 
            chosen = best_state
            current_h = best_h
        else:
            # Không có neighbor tốt hơn, thử lần lượt random trong danh sách
            while candidates:
                h, next_state = random.choice(candidates)
                candidates.remove((h, next_state))  # bỏ neighbor đã thử
                delta = h - current_h
                prob = math.exp(delta / T) if T > 1e-6 else 0
                if random.random() < prob:
                    chosen = next_state
                    current_h = h
                    break
            else:
                # Hết candidates mà không chọn được
                return None

        current = chosen
        path.append(list(current))

        if current == list(solution):
            return path

        # Giảm nhiệt độ
        T *= alpha

    return None
