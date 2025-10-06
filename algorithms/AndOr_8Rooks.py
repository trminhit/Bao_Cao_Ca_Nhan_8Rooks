def AND_OR_SEARCH(N=8, goal=None, mode="goal"):
    """
    OR nodes: lựa chọn hành động nào sẽ thực hiện (ví dụ chọn cột nào).
    AND nodes: tất cả điều kiện con phải thỏa mãn (ví dụ tất cả quân phải được đặt mà không xung đột).
    Thuật toán duyệt qua cây này để tìm goal hoặc tất cả goal.
    """
    def generate(state=(0, []), occupied=set()):
        row, cols = state
        if row == N:
            yield cols
            return

        for col in range(N):  # thử tất cả cột
            if col in occupied:
                continue  # skip ô đã chiếm
            
            # Đây là nondeterministic: vẫn yield tất cả cột khả thi
            new_cols = cols + [col]
            new_occupied = occupied | {col}
            yield from generate((row + 1, new_cols), new_occupied)

    gen = generate()

    if mode == "goal":
        # Lấy goal đầu tiên
        for g in gen:
            if goal is None or g == goal:
                return g
        return None
    else:
        # mode all: in từng bước
        all_goals = []
        for g in gen:
            all_goals.append(g)
        return all_goals
