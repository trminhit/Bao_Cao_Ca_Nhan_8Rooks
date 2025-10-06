import random

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

    def FC_Backtrack(state, domains):
        row = len(state)  # biến hiện tại là hàng row
        if mode == "all":
            all_states.append(state.copy())  # lưu state hiện tại

        if row == n:  # đã đặt đủ n quân
            if mode == "goal" and state == solution:
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
            state.append(col)

            # Forward Checking: giảm domain của các hàng chưa gán
            pruned = []  # lưu lại những giá trị bị loại để restore khi backtrack
            valid = True
            for r in range(row+1, n):
                if col in domains[r]:
                    domains[r].remove(col)
                    pruned.append(r)
                    if not domains[r]:  # nếu domain rỗng => prune nhánh
                        valid = False
                        break

            if valid:
                result = FC_Backtrack(state, domains)
                if result and mode == "goal":
                    return True

            # Backtrack: restore domain
            for r in pruned:
                domains[r].append(col)
            state.pop()  # xóa giá trị vừa thử

        return False

    FC_Backtrack([], initial_domains)
    if mode == "all":
        return all_states
    else:
        return solution
