from .DLS_8Rooks import DepthLimitedSearch

def IDS(solution, mode="goal"):
    all_states = [] if mode == "all" else None
    tracker_stats = None

    for limit in range(1, 9):
        result, perf = DepthLimitedSearch(solution, limit, mode=mode)
        tracker_stats = perf  # lưu perf dict lần limit hiện tại

        if mode == "all" and result:
            all_states.extend(result)
        elif mode == "goal" and result:
            return result, perf  # trả về ngay khi tìm thấy goal

    return (all_states, tracker_stats) if mode == "all" else ([], tracker_stats)
