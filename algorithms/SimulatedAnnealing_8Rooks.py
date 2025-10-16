import random
import math
from engine.performance import PerformanceTracker

def H_match(state, solution):
    """Số quân đặt đúng vị trí so với solution (càng nhiều càng tốt)."""
    return sum(1 for i in range(len(state)) if state[i] == solution[i])

def SimulatedAnnealing(solution, T0=50, alpha=0.8, mode="goal"):
    """
    Simulated Annealing cho 8 Rooks
    - state hiện tại: danh sách các cột đã đặt
    - T0: nhiệt độ khởi đầu
    - alpha: hệ số giảm nhiệt
    Trả về tuple: (result, perf_dict)
    """
    n = len(solution)
    current = []
    path = [list(current)] if mode == "all" else None
    T = T0

    tracker = PerformanceTracker("Simulated Annealing")
    tracker.start()
    tracker.add_node()  # node gốc

    for row in range(n):
        # Sinh tất cả neighbor khả thi
        candidates = []
        for col in range(n):
            if col not in current:
                next_state = current + [col]
                h = H_match(next_state, solution)
                candidates.append((h, next_state))

        if not candidates:
            tracker.stop()
            return (path if mode=="all" else [], tracker.get_stats())

        current_h = H_match(current, solution)
        chosen = None

        # Chọn neighbor tốt nhất hoặc chấp nhận neighbor kém theo xác suất
        best_h, best_state = max(candidates, key=lambda x: x[0])

        if best_h > current_h:
            chosen = best_state
            current_h = best_h
        else:
            temp_candidates = candidates.copy()
            random.shuffle(temp_candidates)
            for h, next_state in temp_candidates:
                delta = h - current_h
                prob = math.exp(delta / T) if T > 1e-6 else 0
                if random.random() < prob:
                    chosen = next_state
                    current_h = h
                    break
            if chosen is None:
                tracker.stop()
                return (path if mode=="all" else [], tracker.get_stats())

        current = chosen
        tracker.add_node()

        if mode == "all":
            path.append(list(current))  # lưu bước trung gian

        # Kiểm tra goal
        if current == list(solution):
            tracker.goal_found()
            tracker.stop()
            return (path, tracker.get_stats()) if mode=="all" else (list(current), tracker.get_stats())

        # Giảm nhiệt độ
        T *= alpha

    tracker.stop()
    return (path if mode=="all" else [], tracker.get_stats())
