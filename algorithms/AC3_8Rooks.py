import random
from collections import deque
from engine.performance import PerformanceTracker

def AC3(solution=None, mode="all"):
    n = 8
    all_states = [] if mode == "all" else None

    tracker = PerformanceTracker("AC3")
    tracker.start()

    # Khởi tạo domain cho từng biến
    domains = [list(range(n)) for _ in range(n)]

    # Khởi tạo queue các cung (arcs)
    queue = deque()
    for i in range(n):
        for j in range(n):
            if i != j:
                queue.append((i, j))  # Mỗi cung (i,j) nghĩa là kiểm tra ràng buộc giữa hàng i và j

    # Hàm loại bỏ giá trị không hợp lệ (inconsistent) của xi so với xj
    def remove_inconsistent_values(xi, xj):
        removed = False
        for x in domains[xi][:]:
            # nếu không tồn tại giá trị y trong domain[xj] sao cho xi=x và xj=y hợp lệ
            if not any(x != y for y in domains[xj]):  # điều kiện ràng buộc xi ≠ xj
                domains[xi].remove(x)
                removed = True
        return removed

    # AC-3: lặp cho tới khi queue rỗng
    while queue:
        xi, xj = queue.popleft()
        if remove_inconsistent_values(xi, xj):  # Nếu loại được giá trị
            if not domains[xi]:  # domain trống => không có nghiệm
                tracker.stop()
                return None, tracker.get_stats()
            # thêm các cung liên quan xi với các biến khác để kiểm tra tiếp
            for xk in range(n):
                if xk != xi and xk != xj:
                    queue.append((xk, xi))

    # Backtrack
    def backtrack(state=[], depth=0):
        if depth == n:
            # Đạt solution, lưu và dừng
            if mode in ["all", "goal"] and solution is not None and state == solution:
                tracker.goal_found()
                if mode == "all":
                    all_states.append(state.copy())
                return True
            return False

        for val in random.sample(domains[depth], len(domains[depth])):
            if val not in state:
                tracker.add_node()  # tăng node visited
                state.append(val)
                # Lưu bước trung gian nếu mode all
                if mode == "all":
                    all_states.append(state.copy())
                result = backtrack(state, depth + 1)
                state.pop()
                if result and mode in ["goal", "all"]:
                    return True
        return False

    backtrack()

    tracker.stop()
    tracker.print_stats()

    if mode == "all":
        return all_states, tracker.get_stats()
    elif mode == "goal" and solution is not None:
        return solution, tracker.get_stats()
    else:
        return [random.choice(d) for d in domains], tracker.get_stats()
