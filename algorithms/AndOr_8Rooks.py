def AND_OR_SEARCH(N=8, goal=None):
    # Xây dựng cây AND-OR
    plans = OR_SEARCH((0, []), [], N)

    # Trích toàn bộ goal paths
    all_goals = extract_goals(plans)

    # Loại bỏ trùng lặp bằng set
    unique_goals = [list(g) for g in set(tuple(x) for x in all_goals)]

    # Nếu có goal cần kiểm tra → lọc ra
    if goal is not None:
        return goal if goal in unique_goals else None

    # Nếu không truyền goal → trả toàn bộ
    return unique_goals


def OR_SEARCH(state, path, N=8):
    row, occupied = state
    if row == N:
        return [[]]   # đạt goal
    if state in path:
        return []     # tránh vòng lặp

    solutions = []
    for s in range(N):
        for d in (None, 'L', 'R'):
            col = s
            if d == 'L':
                col = s - 1
            elif d == 'R':
                col = s + 1

            if 0 <= col < N and col not in occupied:
                result_state = (row + 1, occupied + [col])
                subplans = AND_SEARCH([result_state], path + [state], N)
                for sp in subplans:
                    solutions.append([((s, d, col), sp)])
    return solutions


def AND_SEARCH(states, path, N=8):
    all_plans = [[]]
    for s in states:
        subplans = OR_SEARCH(s, path, N)
        if not subplans:
            return []   # một nhánh thất bại thì toàn bộ thất bại
        new_all = []
        for ap in all_plans:
            for sp in subplans:
                new_all.append(ap + [sp])
        all_plans = new_all
    return all_plans


def extract_goals(plans, path=None):
    """Trích toàn bộ goal states (danh sách cột của các quân) từ kế hoạch"""
    if path is None:
        path = []

    goals = []
    for plan in plans:
        if plan == []:  # chạm goal
            goals.append(path.copy())
        else:
            action, sub = plan[0]
            _, _, col = action
            new_path = path + [col]
            goals.extend(extract_goals(sub, new_path))
    return goals


