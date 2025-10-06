from .DLS_8Rooks import DepthLimitedSearch

def IDS(solution, mode="goal"):
    all_states = [] if mode=="all" else None

    for limit in range(1, 9):
        result = DepthLimitedSearch(solution, limit, mode=mode)
        if mode=="all" and result:
            all_states.extend(result)
        elif mode=="goal" and result is not None:
            return result

    return all_states if mode=="all" else None
