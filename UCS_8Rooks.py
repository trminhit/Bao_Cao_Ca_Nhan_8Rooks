import heapq

def RookCost(state, col, solution):
    row = len(state)       
    target_col = solution[row]
    dis = abs(col - target_col)
    cost = dis +1
    return cost

def UniformCostSearch(solution):
    N = len(solution)
    start = ()
    Queue = [(0, start)]  # (cost, state)
    heapq.heapify(Queue)

    while Queue:
        cost, col_select = heapq.heappop(Queue)  # lấy trạng thái chi phí thấp nhất

        if len(col_select) == N:
            if list(col_select) == solution:  
                return cost, list(col_select)
            else:
                continue

        for col in range(N):
            if col not in col_select:  
                new_state = col_select + (col,)  
                new_cost = cost + RookCost(col_select, col, solution)
                heapq.heappush(Queue, (new_cost, new_state))