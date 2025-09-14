def DepthLimitedSearch(solution, limit):
    N = len(solution)
    Stack = [([], 0)]  # (state, depth)

    while Stack:
        state, depth = Stack.pop()

        if len(state) == N:
            if state == solution:
                return state
            continue

        if depth < limit:
            for col in range(N-1, -1, -1):  
                if col not in state:
                    new_state = state + [col]
                    Stack.append((new_state, depth+1))

    return None  
