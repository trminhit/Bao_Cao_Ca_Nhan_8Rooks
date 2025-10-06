def DepthLimitedSearch(solution, limit, mode="goal"):
    return Recursive_DLS([], solution, limit, mode)

def Recursive_DLS(state, solution, limit, mode="goal"):
    if mode == "all":
        steps = [state[:]] if state else []

    if len(state) == len(solution) and state == solution:
        return steps if mode=="all" else state  # trả về state khi mode goal

    if limit == 0:
        return [] if mode=="all" else None

    for col in range(8):
        if col not in state:
            child = state + [col]
            result = Recursive_DLS(child, solution, limit-1, mode)
            if mode == "all":
                steps.extend(result)
            else:
                if result is not None:
                    return result

    return steps if mode=="all" else None
