import DLS_8Rooks

def IDS(solution):
    for limit in range(1, 9):
        result = DLS_8Rooks.DepthLimitedSearch(solution, limit)
        if result is not None:
            return result
    return None
