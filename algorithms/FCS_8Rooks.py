def ForwardChecking_8Rooks(n=8, goal=None, mode="all"):
    """
    Forward checking DFS cho 8 rooks.
    - n: số hàng/quân
    - goal: nếu có, tìm đúng state trùng goal
    - mode: "all" trả về tất cả states, "goal" trả về state cuối cùng đầy đủ
    """
    goal_list = list(goal) if goal is not None else None
    all_states = []

    def forward_check(state, domains):
        if state:
            all_states.append(state[:])  # Lưu state hiện tại

        if len(state) == n:
            if goal_list is not None:
                if state == goal_list:
                    return state
                else:
                    return None
            else:
                return state

        row = len(state)
        for col in list(domains[row]):
            if col not in state:
                # Tạo domains mới
                new_domains = [d[:] for d in domains]
                for r in range(row + 1, n):
                    if col in new_domains[r]:
                        new_domains[r].remove(col)

                if all(len(d) > 0 for r, d in enumerate(new_domains) if r > row):
                    result = forward_check(state + [col], new_domains)
                    if result is not None and mode == "goal":
                        return result

        return None

    domains = [list(range(n)) for _ in range(n)]
    result = forward_check([], domains)
    return all_states if mode == "all" else result
