import random

def Backtracking(solution, mode="all"):
    """
    Thuật toán Backtracking cho bài toán 8 Rooks.
    Variables: mỗi hàng là một biến (len(state) = hàng hiện tại)
    Domains: các cột khả thi (range(n)) sẽ được shuffle để random hóa
    Constraints: không có hai quân nào cùng cột
    """
    n = len(solution)
    all_states = [] if mode == "all" else None

    def Backtrack(state):
        #state hiện tại là danh sách các cột đã đặt, index = hàng hiện tại
        if mode == "all":
            all_states.append(state.copy())  # Lưu trạng thái hiện tại

        #nếu đã đặt đủ n quân
        if len(state) == n:
            if state == solution:  
                return True 
            else:
                return False  

        # tạo danh sách cột khả thi cho hàng hiện tại
        candidates = list(range(n))
        random.shuffle(candidates)  # Random thứ tự cột

        # thử từng cột trong candidates
        for col in candidates:
            if col not in state:  # Ràng buộc: không trùng cột
                state.append(col)  # Gán giá trị biến
                # Đệ quy sang biến tiếp theo (hàng tiếp theo)
                result = Backtrack(state)
                if result and mode == "goal": 
                    return True
                state.pop()  # Backtrack: xóa giá trị vừa thử

        return False  # Nếu hết candidates mà không thành công

    Backtrack([]) 
    if mode == "all":
        return all_states  
    else:
        return solution 
