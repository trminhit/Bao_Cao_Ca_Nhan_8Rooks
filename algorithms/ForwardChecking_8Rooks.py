import random
from engine.performance import PerformanceTracker

def ForwardChecking(solution, mode="all"):
    """
    Forward Checking cho 8 Rooks:
    - Variables: mỗi hàng là một biến
    - Domains: cột khả thi còn lại
    - Constraints: không có 2 quân cùng cột
    """
    n = len(solution)
    all_states = [] if mode == "all" else None

    # Khởi tạo domain cho từng hàng
    initial_domains = [list(range(n)) for _ in range(n)]

    tracker = PerformanceTracker("ForwardChecking")
    tracker.start()

    def FC_Backtrack(state, domains):
        row = len(state)
          # tăng node visited

        if mode == "all":
            all_states.append(state.copy())

        if row == n:
            if mode == "goal" and state == solution:
                tracker.goal_found()
                return True
            elif mode == "goal":
                return False
            else:
                return True

        # Lấy domain hiện tại và random hóa thứ tự thử
        candidates = domains[row].copy()
        random.shuffle(candidates)

        for col in candidates:
            # thử gán col cho row
            tracker.add_node()
            state.append(col)

            pruned = []
            valid = True
            for r in range(row + 1, n):
                if col in domains[r]:
                    domains[r].remove(col)
                    pruned.append(r)
                    if not domains[r]:
                        valid = False
                        break

            if valid:
                result = FC_Backtrack(state, domains)
                if result and mode == "goal":
                    return True

            # restore domain
            for r in pruned:
                domains[r].append(col)
            state.pop()

        return False

    FC_Backtrack([], initial_domains)
    tracker.stop()
    tracker.print_stats()
    if mode == "all":
        return all_states, tracker.get_stats()
    else:
        return solution, tracker.get_stats()
