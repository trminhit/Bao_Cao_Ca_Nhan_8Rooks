def DepthLimitedSearch(solution, limit):
    return Recursive_DLS([], solution, limit)

def Recursive_DLS(state, solution, limit):
    
    if len(state) == len(solution) and state == solution:
        return state
    
    if limit == 0:
        return None
    
    row = len(state)   
    
    for col in range(8):
        if col not in state: 
            child = state + [col]
            result = Recursive_DLS(child, solution, limit - 1)
            if result is not None:
                return result
    return None

