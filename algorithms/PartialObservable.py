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


def successors(state, n, prefix_len):
    successors_list = []
    row = len(state)

    # Move
    if row > prefix_len:
        for r in range(prefix_len, row):
            for col in range(n):
                if col != state[r] and col not in state:
                    new_state = state.copy()
                    new_state[r] = col
                    successors_list.append(new_state)
                    break
            if successors_list:
                break

    # Place
    if row < n:
        for col in range(n):
            if col not in state:
                successors_list.append(state + [col])
                break

    return successors_list


def Find_Rooks_DFS_Belief(solution, mode="all", seed=None):
    n = len(solution)

    perf = PerformanceTracker("Partial Observable DFS")
    perf.start()

    start_belief = make_start_belief(solution, k=5, extra_states=2, seed=seed)
    goal_beliefs = make_goal_beliefs(solution, num_goals=5, seed=seed)

    visited = set()
    path = []  # lưu lại các belief đã đi qua
    stack = [start_belief]  # stack khởi đầu với 1 belief (list các state)

    while stack:
        belief = stack.pop()
        key = tuple(tuple(state) for state in belief)
        if key in visited:
            continue
        visited.add(key)
        path.append(belief)
        perf.add_node(len(belief))

        # check goal
        conds = [len(state) == n and state in goal_beliefs for state in belief]
        if any(conds):
            perf.goal_found()
            perf.stop()
            
            if mode == "all":
                # Trả về (path, perf_dict) cho visualize
                return (path, perf.get_stats())
            elif mode == "goal":
                # Trả về (final_state, perf_dict) cho start
                for state in belief:
                    if len(state) == n and state in goal_beliefs:
                        return (state, perf.get_stats())

        # mở rộng successors
        new_belief = []
        for state in belief:
            for s in successors(state, n, prefix_len=5):
                if s not in new_belief:
                    new_belief.append(s)

        if new_belief:
            stack.append(new_belief)

    # Kết thúc vòng lặp mà không tìm thấy goal
    perf.stop()
    
    if mode == "all":
        return (path, perf.get_stats())
    elif mode == "goal":
        # Trả về state cuối cùng trong belief cuối cùng
        final_state = path[-1][0] if path and path[-1] else []
        return (final_state, perf.get_stats())