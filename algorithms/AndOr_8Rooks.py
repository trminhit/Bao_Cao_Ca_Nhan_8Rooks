from engine.performance import PerformanceTracker

def AND_OR_SEARCH(N=8, goal=None, mode="goal"):
    """
    OR nodes: lựa chọn hành động nào sẽ thực hiện (ví dụ chọn cột nào).
    AND nodes: tất cả điều kiện con phải thỏa mãn (ví dụ tất cả quân phải được đặt mà không xung đột).
    Thuật toán duyệt qua cây này để tìm goal hoặc tất cả goal.
    """

    tracker = PerformanceTracker("AND-OR Search")
    tracker.start()

    def generate(state=(0, []), occupied=set()):
        row, cols = state
        if row == N:
            tracker.add_node()  # mỗi goal đếm như 1 node
            yield cols
            return

        for col in range(N):  # thử tất cả cột
            if col in occupied:
                continue  # skip ô đã chiếm
            
            # Đây là nondeterministic: yield tất cả cột khả thi
            new_cols = cols + [col]
            new_occupied = occupied | {col}
            yield from generate((row + 1, new_cols), new_occupied)

    gen = generate()

    if mode == "goal":
        # Lấy goal đầu tiên
        for g in gen:
            if goal is None or g == goal:
                tracker.goal_found()
                tracker.stop()
                return g, tracker.get_stats()
        tracker.stop()
        return None, tracker.get_stats()
    else:
        # mode all: in từng bước
        all_goals = []
        for g in gen:
            all_goals.append(g)
        tracker.stop()
        return all_goals, tracker.get_stats()
