from .DLS_8Rooks import DepthLimitedSearch

def IDS(solution):
    for limit in range(1, 9):
        result = DepthLimitedSearch(solution, limit)
        if result is not None:
            return result
    return None
