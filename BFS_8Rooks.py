def Find_Rooks():
    start = []
    Queue = [start]
    
    while Queue:
        col_select = Queue.pop(0)
        if len(col_select) == 8:
            return [(i, col_select[i]) for i in range(len(col_select))]
        
        for col in range(8):
            if col not in col_select:
                new_state = col_select + [col]
                Queue.append(new_state)
