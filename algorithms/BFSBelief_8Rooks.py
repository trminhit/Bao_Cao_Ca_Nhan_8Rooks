from collections import deque

def bfs_belief(N=8, goal=None):
    # Mỗi trạng thái là danh sách các cột đã đặt quân 
    initial_state = []  
    # Queue lưu belief state
    queue = deque()
    queue.append([initial_state])  # ban đầu chỉ có 1 trạng thái khả dĩ

    visited_belief_states = set()  # tránh lặp lại

    while queue:
        belief = queue.popleft()
        # Nếu tất cả state trong belief đều đã đầy đủ (goal)
        for state in belief:
            if len(state) == N:
                if goal is None or state == goal:
                    return state  # tìm thấy solution
        # Sinh belief state tiếp theo
        next_belief = []
        for state in belief:
            row = len(state)
            for col in range(N):
                if col not in state:  # hợp lệ
                    next_belief.append(state + [col])
        # Chuyển next_belief thành tuple 
        belief_tuple = tuple(tuple(s) for s in next_belief)
        if belief_tuple not in visited_belief_states:
            visited_belief_states.add(belief_tuple)
            queue.append(next_belief)
    return None

