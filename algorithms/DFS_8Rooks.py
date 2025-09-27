# def Find_Rooks_DFS(solution):
#     start = []
#     Stack = [start]
    
#     while Stack:
#         col_select = Stack.pop()
#         # yield trạng thái hiện tại (có thể chưa đủ 8 quân)
#         yield [(i, col_select[i]) for i in range(len(col_select))]
        
#         if len(col_select) == 8:
#             if col_select == solution:
#                 break
#             else:
#                 continue
        
#         for col in range(7, -1, -1):  
#             if col not in col_select:
#                 new_state = col_select + [col]
#                 Stack.append(new_state)
        
def Find_Rooks_DFS(solution):
    Stack = [[]]

    while Stack:
        col_select = Stack.pop()
        if len(col_select) == len(solution):
            if col_select == solution:
                return [(i, col_select[i]) for i in range(len(col_select))]
            else:
                continue

        for col in range(7, -1, -1):
            if col not in col_select:
                Stack.append(col_select + [col])