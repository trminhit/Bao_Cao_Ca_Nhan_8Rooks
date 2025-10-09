import time
from engine.performance import PerformanceTracker
N = 8  

def successors(state):
    """Sinh các successor của một state (chỉ state, không cần action)."""
    n = N
    successors_list = []

    # Move: di chuyển quân hiện tại
    if state:
        for r in range(len(state)):
            for col in range(n):
                if col != state[r] and col not in state:
                    new_state = state.copy()
                    new_state[r] = col
                    successors_list.append(new_state)
                    break
            if successors_list:
                break
            
    # Place: thêm quân mới nếu chưa đủ n
    if len(state) < n:
        for col in range(n):
            if col not in state:
                new_state = state + [col]
                successors_list.append(new_state)
                break

    return successors_list

def make_start_belief(n=8):
    start_belief = [[]]  # State rỗng
    
    # Thêm các state có 1 quân ở mỗi cột
    for col in range(n):
        start_belief.append([col])
    
    return start_belief


def is_valid_goal_state(state, n=8):
    if len(state) != n:
        return False
    return set(state) == set(range(n))


def update_belief_move(belief, n):
    move_belief = []
    
    for state in belief:
        for successor in successors(state):
            # Chỉ lấy move (cùng độ dài)
            if len(successor) == len(state):
                if successor not in move_belief:
                    move_belief.append(successor)
                break  # Chỉ lấy 1 move successor
    
    return move_belief


def update_belief_place(belief, n):
    place_belief = []
    
    for state in belief:
        for successor in successors(state):
            # Chỉ lấy place (độ dài tăng)
            if len(successor) > len(state):
                if successor not in place_belief:
                    place_belief.append(successor)
                break  # Chỉ lấy 1 place successor
    
    return place_belief


def is_goal_belief(belief, goal, n):
    """
    - Tất cả trạng thái trong tập belief phải thuộc tập goal belief
    - Nếu có goal cụ thể và tìm thấy state khớp → trả về state đó
    - Nếu không có goal cụ thể hoặc không tìm thấy → trả về state đầu tiên

    """
    if not belief:
        return False, None
    
    for state in belief:
        if not is_valid_goal_state(state, n):
            return False, None
    
    if goal is not None:
        for state in belief:
            if state == goal:
                return True, state  # Tìm thấy solution khớp goal
    # Trả về state đầu tiên trong belief
    return True, belief[0]


def dfs_belief_generator(start_belief, goal, n, tracker=None):
    """
    Yields:(belief, perf) - tuple của belief hiện tại và performance stats
    """
    stack = [start_belief]
    visited_beliefs = set()
    
    while stack:
        belief = stack.pop()
        
        # Convert to hashable để check visited
        key = tuple(tuple(state) for state in belief)
        if key in visited_beliefs:
            continue
        visited_beliefs.add(key)
        
        # Track nodes
        if tracker:
            tracker.add_node(len(belief))  # mỗi belief có thể chứa nhiều state
            perf = tracker.get_stats()
        else:
            perf = {"nodes_visited": 0, "elapsed_time": 0}
        
        # Kiểm tra goal
        is_goal, goal_state = is_goal_belief(belief, goal, n)
        perf["solution_found"] = is_goal
        
        # tập các states
        yield belief, perf
        
        # DỪNG KHI TẤT CẢ STATES TRONG BELIEF ĐỀU LÀ GOAL
        if is_goal:
            return
        
        # Sinh 2 ACTIONS: Move và Place
        move_belief = update_belief_move(belief, n)
        place_belief = update_belief_place(belief, n)
        
        # PUSH: Move trước, Place sau (Place sẽ pop trước - LIFO)
        if move_belief:
            stack.append(move_belief)
        if place_belief:
            stack.append(place_belief)


def Find_Rooks_DFS_Belief(goal=None, mode="goal"):
    """
    Đặc điểm:
    - Start belief động: [[], [0], [1], ..., [7]]
    - Goal beliefs: TẤT CẢ permutations hợp lệ (dùng hàm kiểm tra)
    - Strong goal: TẤT CẢ states trong belief phải là goal
    - Dừng khi: Tìm được belief mà tất cả states đều là goals
    - Output: State khớp goal (nếu có) hoặc state đầu tiên
    """
    n = N
    tracker = PerformanceTracker("Unobservable DFS")
    tracker.start()
    
    # 1. Khởi tạo Start Belief động
    start_belief = make_start_belief(n)
    
    # 2. DFS với belief states
    if mode == "goal":
        final_state = None
        final_perf = {}
        
        for belief, perf in dfs_belief_generator(start_belief, goal, n, tracker):
            if perf.get("solution_found", False):
                # Tìm thấy goal
                is_goal, goal_state = is_goal_belief(belief, goal, n)
                if is_goal:
                    final_state = goal_state
                    tracker.goal_found()
                    final_perf = tracker.get_stats()
                    final_perf["solution_found"] = True
                    break
        
        tracker.stop()
        final_perf = tracker.get_stats()
        final_perf["solution_found"] = bool(final_state)
        
        return final_state or [], final_perf
    
    else:  # mode == "all"
        all_beliefs = []
        last_perf = {}
        
        for belief, perf in dfs_belief_generator(start_belief, goal, n, tracker):
            all_beliefs.append(belief)
            last_perf = perf
        
        tracker.stop()
        last_perf = tracker.get_stats()
        
        return all_beliefs, last_perf


def beliefs_to_states(beliefs):
    """
    Convert list of beliefs thành list of single states để dễ animate.
    Lấy state đầu tiên từ mỗi belief.
    Args:
        beliefs: List of beliefs [[state1, state2, ...], [state3, state4, ...], ...]
    Returns:
        List of single states [state1, state3, ...]
    """
    states = []
    for belief in beliefs:
        if belief:
            states.append(belief[0])  # Lấy state đầu tiên
    return states


def belief_to_all_states(belief):
    """
    Convert 1 belief thành list tất cả states trong belief.
    Dùng để visualize tất cả khả năng cùng lúc.
    Args:
        belief: List of states [state1, state2, state3, ...]
    Returns:
        List of states [state1, state2, state3, ...]
    """
    return belief
