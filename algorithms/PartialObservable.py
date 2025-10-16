import random
import itertools
from engine.performance import PerformanceTracker  


def make_start_belief(solution, k=5, extra_states=2, seed=None):
    """
    Start belief: mỗi state giữ k dòng đầu của solution
    - State 1: k dòng đầu
    - State i (i>=2): k dòng đầu + (i-1) quân random
    """
    if seed is not None:
        random.seed(seed)

    n = len(solution)
    base = solution[:k]
    start_belief = [base]

    available = [c for c in range(n) if c not in base]

    for i in range(1, extra_states + 1):
        cols = available[:]
        random.shuffle(cols)
        extra = cols[:i]
        state_i = base + extra
        start_belief.append(state_i)

    return start_belief


def make_goal_beliefs(solution, num_goals=5, k=5, seed=None):
    """
    Goal beliefs: giữ k dòng đầu giống solution
    - Thêm các perm random cho phần còn lại
    """
    if seed is not None:
        random.seed(seed)

    n = len(solution)
    prefix = solution[:k]
    remaining = [c for c in range(n) if c not in prefix]

    all_perms = list(itertools.permutations(remaining))
    random.shuffle(all_perms)

    goals = []
    for perm in all_perms:
        goals.append(prefix + list(perm))
        if len(goals) >= num_goals:
            break
    return goals


def belief_move(belief, n, prefix_len):
    """Sinh belief mới bằng hành động MOVE:
       - Mỗi state move 1 quân (từ hàng >= prefix_len)
       - State full thì giữ nguyên"""
    new_belief = []

    for state in belief:
        if len(state) == n:
            # full rồi thì giữ nguyên
            new_belief.append(state)
            continue

        moved = False
        # chỉ move được nếu có hàng >= prefix_len
        if len(state) > prefix_len:
            for r in range(prefix_len, len(state)):
                for col in range(n):
                    if col != state[r] and col not in state:
                        new_state = state.copy()
                        new_state[r] = col
                        new_belief.append(new_state)
                        moved = True
                        break
                if moved:
                    break
        if not moved:
            # nếu không move được (hoặc chưa đủ hàng để move)
            new_belief.append(state)
    return new_belief


def belief_place(belief, n):
    """Sinh belief mới bằng hành động PLACE:
       - Mỗi state thêm 1 quân mới nếu chưa full"""
    new_belief = []
    for state in belief:
        if len(state) < n:
            for col in range(n):
                if col not in state:
                    new_belief.append(state + [col])
                    break
        else:
            # full thì giữ nguyên
            new_belief.append(state)
    return new_belief


def Find_Rooks_DFS_Belief(solution, mode="all", seed=None):
    """DFS Belief với 2 hành động: MOVE -> PLACE, goal check toàn bộ belief"""
    n = len(solution)
    perf = PerformanceTracker("Partial Observable DFS")
    perf.start()

    start_belief = make_start_belief(solution, k=5, extra_states=2, seed=seed)
    goal_beliefs = make_goal_beliefs(solution, num_goals=5, seed=seed)

    visited = set()
    path = []
    stack = [start_belief]  # khởi đầu stack với belief đầu tiên

    prefix_len = 4

    while stack:
        belief = stack.pop()
        key = tuple(tuple(s) for s in belief)
        if key in visited:
            continue
        visited.add(key)
        path.append(belief)
        perf.add_node(len(belief))

        # kiểm tra toàn bộ belief 
        if all(len(s) == n and s in goal_beliefs for s in belief):
            perf.goal_found()
            perf.stop()
            if mode == "all":
                return (path, perf.get_stats())
            else:
                return (belief[0], perf.get_stats())  # tất cả states đều đúng, trả state đầu tiên

        # mở rộng belief theo 2 hành động
        move_belief = belief_move(belief, n, prefix_len)
        place_belief = belief_place(belief, n)

        # push MOVE trước rồi PLACE sau (để PLACE được xử lý trước)
        stack.append(move_belief)
        stack.append(place_belief)

    perf.stop()

    if mode == "all":
        return (path, perf.get_stats())
    else:
        final_state = path[-1][0] if path and path[-1] else []
        return (final_state, perf.get_stats())
