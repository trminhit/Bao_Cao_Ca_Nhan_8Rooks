# from engine.performance import PerformanceTracker

# def nondet_successors(state, n):
#     """
#     Sinh các kết quả có thể xảy ra khi thực hiện hành động PlaceRook.
#     """
#     row = len(state)
#     results = []
#     valid_cols = [c for c in range(n) if c not in state]
#     for col in valid_cols:
#         succ = []
#         # Kết quả 1: Thành công
#         succ.append(state + [col])
#         # Kết quả 2: Thất bại (đặt trượt vào các cột trống khác)
#         other_cols = [c for c in valid_cols if c != col]
#         for pushed in other_cols:
#             succ.append(state + [pushed])
#         results.append((col, succ))
#     return results

# def AND_OR_SEARCH(N=8, goal=None, mode="all"):
#     """
#     AND-OR search hoàn chỉnh, kết hợp Ghi nhớ (Memoization) và Phát hiện chu trình (Cycle Detection).
#     """
#     tracker = PerformanceTracker("Nondeterministic Planner (Optimized + Cycle Check)")
#     tracker.start()

#     memo = {}
#     steps_visual = []

#     # Hàm đệ quy giờ đây nhận thêm `path` để theo dõi đường đi hiện tại
#     def recursive_search(state, path):
#         key = tuple(state)

#         # 1. Tối ưu Ghi nhớ: Nếu bài toán con đã được giải, trả về kết quả ngay
#         if key in memo:
#             return memo[key]
        
#         # 2. Phát hiện chu trình: Nếu trạng thái đã có trên đường đi, đây là vòng lặp -> thất bại
#         if key in path:
#             return None # FAILURE (CYCLE DETECTED)

#         # Ghi lại bước duyệt để visualize (chỉ ghi lần đầu tiên duyệt)
#         steps_visual.append(list(state))
#         tracker.add_node()
        
#         if len(state) == N:
#             return "GOAL"

#         # Tạo đường đi mới cho các nhánh con, bao gồm cả trạng thái hiện tại
#         new_path = path | {key}

#         # OR-node: thử từng hành động
#         for action, outcomes in nondet_successors(state, N):
#             subplans = []
#             all_success = True
#             # AND-node: mọi kết quả đều phải có kế hoạch
#             for result_state in outcomes:
#                 # Truyền `new_path` xuống cho các lời gọi đệ quy
#                 subplan = recursive_search(result_state, new_path)
#                 if subplan is None:
#                     all_success = False
#                     break
#                 subplans.append((result_state, subplan))
            
#             if all_success:
#                 plan = {"action": action, "results": subplans}
#                 memo[key] = plan # Lưu kết quả thành công vào bảng ghi nhớ
#                 return plan
        
#         memo[key] = None # Lưu kết quả thất bại vào bảng ghi nhớ
#         return None

#     # Bắt đầu tìm kiếm với trạng thái rỗng và đường đi rỗng
#     plan = recursive_search([], set())
#     tracker.stop()

#     # Phần xử lý kết quả giữ nguyên như trước
#     is_goal_achievable = False
#     if plan:
#         solutions = extract_all_solutions(plan)
#         if goal and goal in solutions:
#             is_goal_achievable = True

#     if is_goal_achievable:
#         tracker.goal_found()

#     if mode == "goal":
#         final_solution = goal if is_goal_achievable else None
#         return final_solution, tracker.get_stats()
#     else: # mode == "all"
#         return steps_visual, tracker.get_stats()

# def extract_all_solutions(plan):
#     solutions = []
#     def dfs(node):
#         if isinstance(node, dict):
#             for state, subplan in node["results"]:
#                 if subplan == "GOAL":
#                     if state not in solutions:
#                          solutions.append(state)
#                 else:
#                     dfs(subplan)
#     dfs(plan)
#     return solutions

from engine.performance import PerformanceTracker

# def nondet_successors(state, n):
#     """
#     --- ĐÃ SỬA ĐỔI THEO ĐÚNG YÊU CẦU ---
#     Sinh các kết quả có thể xảy ra khi thực hiện hành động PlaceRook.
#     Kết quả 1: Thành công.
#     Kết quả 2: Thất bại (có thể trượt sang TẤT CẢ các ô trống khác).
#     """
#     row = len(state)
#     results = []
#     valid_cols = [c for c in range(n) if c not in state]
#     for col in valid_cols:
#         succ = []
#         # Kết quả 1: Thành công
#         succ.append(state + [col])
#         # Kết quả 2: Thất bại (liệt kê tất cả các trường hợp trượt)
#         other_cols = [c for c in valid_cols if c != col]
#         for pushed in other_cols:
#             succ.append(state + [pushed])
#         results.append((col, succ))
#     return results
def nondet_successors(state, n):
    """
    Sinh các kết quả có thể xảy ra khi thực hiện hành động PlaceRook.
    """
    row = len(state)
    results = []
    valid_cols = [c for c in range(n) if c not in state]
    for col in valid_cols:
        succ = []
        # Kết quả 1: Thành công
        succ.append(state + [col])
        # Kết quả 2: Thất bại (đặt trượt vào các cột trống khác)
        other_cols = [c for c in valid_cols if c != col]
        for pushed in other_cols:
            succ.append(state + [pushed])
        results.append((col, succ))
    return results

def AND_OR_SEARCH(N=8, goal=None, mode="all"):
    """
    AND-OR search hoàn chỉnh, đáp ứng tất cả các yêu cầu về logic trả về.
    """
    tracker = PerformanceTracker("Nondeterministic Planner (Final)")
    tracker.start()

    memo = {}
    steps_visual = []

    def recursive_search(state, path):
        key = tuple(state)
        
        # 1. Tối ưu Ghi nhớ (Toàn cục)
        if key in memo:
            return memo[key]
        
        # 2. Phát hiện chu trình (Cục bộ)
        if key in path:
            return None # FAILURE (CYCLE DETECTED)

        if key not in memo: # Chỉ ghi lại bước duyệt lần đầu tiên
            steps_visual.append(list(state))
            tracker.add_node()
        
        if len(state) == N:
            return "GOAL"

        new_path = path | {key}

        # OR-node: Dừng lại khi tìm thấy MỘT hành động thành công
        for action, outcomes in nondet_successors(state, N):
            subplans = []
            all_success = True
            # AND-node: Mọi kết quả đều phải có kế hoạch
            for result_state in outcomes:
                subplan = recursive_search(result_state, new_path)
                if subplan is None:
                    all_success = False
                    break
                subplans.append((result_state, subplan))
            
            if all_success:
                plan = {"action": action, "results": subplans}
                memo[key] = plan
                return plan # Dừng lại ngay khi tìm thấy một lựa chọn OR thành công
        
        memo[key] = None
        return None

    # Bắt đầu tìm kiếm
    plan = recursive_search([], set())
    tracker.stop()

    # --- XỬ LÝ KẾT QUẢ TRẢ VỀ THEO YÊU CẦU ---
    
    final_solution = None
    if plan:
        solutions = extract_all_solutions(plan)
        if solutions: # Nếu kế hoạch có thể dẫn đến ít nhất một lời giải
            if goal and goal in solutions:
                # Ưu tiên 1: Lời giải mong muốn có trong kết quả
                final_solution = goal
            else:
                # Ưu tiên 2: Lấy lời giải đầu tiên tìm được
                final_solution = solutions[0]

    if final_solution:
        tracker.goal_found()

    # Trả về kết quả tùy theo mode
    if mode == "goal":
        # Trả về lời giải đã được chọn (hoặc None nếu thất bại)
        return final_solution, tracker.get_stats()
    else: # mode == "all"
        # Luôn trả về toàn bộ quá trình duyệt để visualize
        return steps_visual, tracker.get_stats()

def extract_all_solutions(plan):
    solutions = []
    def dfs(node):
        if isinstance(node, dict):
            for state, subplan in node["results"]:
                if subplan == "GOAL":
                    if state not in solutions:
                         solutions.append(state)
                else:
                    dfs(subplan)
    dfs(plan)
    return solutions