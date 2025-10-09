def H_match(state, solution):
    """Số quân đặt đúng vị trí so với solution (càng nhiều càng tốt)"""
    return sum(1 for i in range(len(state)) if state[i] == solution[i])

from engine.performance import PerformanceTracker

def HillClimbing(solution, mode="goal"):
    """
    Hill Climbing cho 8 Rooks
    - mode == "all": trả về tất cả states trung gian
    - mode == "goal": trả về state cuối cùng nếu tìm thấy, [] nếu không
    """
    n = len(solution)
    current = []
    path = [list(current)] if mode == "all" else None

    tracker = PerformanceTracker("Hill Climbing")
    tracker.start()
    tracker.add_node()  # node gốc

    for row in range(n):
        candidates = []
        for col in range(n):
            if col not in current:  # constraint: không trùng cột
                next_state = current + [col]
                h = H_match(next_state, solution)
                candidates.append((h, next_state))

        if not candidates:
            tracker.stop()
            return (path if mode=="all" else [], tracker.get_stats())  # hết nước đi

        # chọn neighbor có h lớn nhất
        best_h, best_state = max(candidates, key=lambda x: x[0])
        current_h = H_match(current, solution)

        # nếu không cải thiện -> dừng
        if best_h <= current_h:
            tracker.stop()
            return (path if mode=="all" else [], tracker.get_stats())

        current = best_state
        tracker.add_node()  # mỗi lần chọn state mới

        if mode == "all":
            path.append(list(current))  # lưu bước trung gian

        # kiểm tra đạt goal
        if current == list(solution):
            tracker.goal_found()
            tracker.stop()
            return (path, tracker.get_stats()) if mode=="all" else (list(current), tracker.get_stats())

    tracker.stop()
    return (path if mode=="all" else [], tracker.get_stats())
