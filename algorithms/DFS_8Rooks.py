def Find_Rooks_DFS(solution, mode="all"):
    """DFS cho bài toán 8 Rooks"""
    Stack = [[]]
    states = [] if mode == "all" else None

    while Stack:
        col_select = Stack.pop()

        # Lưu state hiện tại nếu mode="all"
        if mode == "all":
            states.append(col_select[:])

        # Kiểm tra goal
        if len(col_select) == len(solution):
            if col_select == solution:
                if mode == "all":
                    return states
                return col_select[:]  # mode="goal"
            continue

        # Thêm các bước tiếp theo vào stack
        for col in range(7, -1, -1):  # DFS từ cột lớn xuống nhỏ
            if col not in col_select:
                Stack.append(col_select + [col])

    return states if mode == "all" else []
