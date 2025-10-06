def successors(state, n):
    successors = []
    row = len(state)

    # Move: Chỉ lấy một successor đầu tiên nếu có
    if state:
        for r in range(row):
            for col in range(n):
                if col != state[r] and col not in state:
                    new_state = state.copy()
                    new_state[r] = col
                    successors.append(new_state)
                    break
            if successors:
                break

    # Place: Chỉ lấy một successor đầu tiên nếu có
    if row < n:
        for col in range(n):
            if col not in state:
                successors.append(state + [col])
                break
    
    return successors
def Find_Rooks_DFS_Belief(solution, mode="all"):
    """DFS với belief states cho bài toán 8 Rooks"""
    start_belief = [[], [2]]  # Belief ban đầu
    goal_beliefs = [
        [0, 1, 2, 3, 4, 5, 6, 7],
        solution,  # Goal truyền vào
        [0, 3, 2, 1, 4, 5, 7, 6]
    ]
    n = 8  # Kích thước bàn cờ 8x8

    stack = [start_belief]
    steps = [] if mode == "all" else None
    
    while stack:
        belief = stack.pop()
        
        if mode == "all":
            steps.append(belief)

        # Kiểm tra nếu toàn bộ state trong belief thuộc goal_beliefs
        conds = [len(state) == n and state in goal_beliefs for state in belief]
        if all(conds):
            # Ưu tiên trạng thái khớp với solution
            for state in belief:
                if state == solution:
                    if mode == "all":
                        return steps
                    return state[:]  
            if mode == "all":
                return steps
            return belief[0][:] if belief else []
        
        # Sinh belief mới từ move và place
        move_belief = []
        place_belief = []
        for state in belief:
            for ns in successors(state, n):
                if len(ns) == len(state):  # Move
                    move_belief.append(ns)
                else:  # Place
                    place_belief.append(ns)
        if move_belief:
            stack.append(move_belief)
        if place_belief:
            stack.append(place_belief)    
    
    return steps if mode == "all" else []

