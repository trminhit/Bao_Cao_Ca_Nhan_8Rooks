# def Find_Rooks_BFS(solution):
#     start = []
#     Queue = [start]
    
#     while Queue:
#         col_select = Queue.pop(0)
#         # yield trạng thái hiện tại (có thể chưa đủ 8 quân)
#         yield [(i, col_select[i]) for i in range(len(col_select))]
        
#         if len(col_select) == 8:
#             if col_select == solution:
#                 break
#             else:
#                 continue
        
#         for col in range(8):
#             if col not in col_select:
#                 new_state = col_select + [col]
#                 Queue.append(new_state)

def Find_Rooks_BFS(solution):
    Queue = [[]]
    while Queue:
        col_select = Queue.pop(0)
        if len(col_select) == len(solution):
            if col_select == solution:
                return [(i, col_select[i]) for i in range(len(col_select))]
            else:
                continue

        for col in range(8):
            if col not in col_select:
                Queue.append(col_select + [col])

