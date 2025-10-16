from engine.common_goal import check_goal, handle_goal_found
from engine.performance import PerformanceTracker

def IDS(solution, mode="all"):
    """
    Tìm kiếm sâu dần (Iterative Deepening Search).
    """
    tracker = PerformanceTracker("IDS")
    tracker.start()
    
    all_states_path = []

    # Vòng lặp chính của IDS, tăng dần độ sâu giới hạn
    for limit in range(1, len(solution) + 1):
        
        # Hàm đệ quy thực hiện tìm kiếm giới hạn độ sâu (DLS)
        def _dls_recursive(state, current_limit):
            tracker.add_node()

            if mode == "all":
                all_states_path.append(state[:])

            # Kiểm tra nếu đạt được mục tiêu
            if check_goal(state, solution):
                tracker.goal_found()
                return state[:] 
            
            # Dừng nếu đã hết giới hạn độ sâu
            if current_limit == 0:
                return None

            # Sinh các trạng thái con và gọi đệ quy
            for col in range(len(solution)):
                if col not in state:
                    child = state + [col]
                    result = _dls_recursive(child, current_limit - 1)
                    
                    # Nếu tìm thấy lời giải ở nhánh con, trả về ngay lập tức
                    if result is not None:
                        return result
            
            return None # Không tìm thấy lời giải trong nhánh này

        # Bắt đầu tìm kiếm DLS với độ sâu limit hiện tại
        result = _dls_recursive([], limit)
        
        if result:
            tracker.stop()
            return handle_goal_found(mode, all_states_path, result, tracker)

    tracker.stop()
    return (all_states_path, tracker.get_stats()) if mode == "all" else ([], tracker.get_stats())