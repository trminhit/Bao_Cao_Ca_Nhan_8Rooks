def Find_Rooks_BFS(solution, mode="all"):
    Queue = [[]]
    states = [] if mode == "all" else None
    
    while Queue:
        col_select = Queue.pop(0)
        
        if mode == "all":
            states.append(col_select[:])  # Lưu trạng thái hiện tại (mảng 1 chiều)
        
        if len(col_select) == len(solution):
            if col_select == solution:
                if mode == "all":
                    return states
                return col_select[:]  # Trả về mảng 1 chiều cho mode="goal"
            continue

        for col in range(8):
            if col not in col_select:
                Queue.append(col_select + [col])
    
    return states if mode == "all" else []