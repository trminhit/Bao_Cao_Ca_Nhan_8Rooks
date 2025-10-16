from engine.common_goal import check_goal
from engine.performance import PerformanceTracker

def DepthLimitedSearch(solution, limit, mode="goal"):
    tracker = PerformanceTracker("DLS")
    tracker.start()

    result = Recursive_DLS([], solution, limit, mode, tracker)

    tracker.stop()
    if mode == "all":
        return result, tracker.get_stats()
    else:
        return (result, tracker.get_stats()) if result is not None else ([], tracker.get_stats())


def Recursive_DLS(state, solution, limit, mode="goal", tracker=None):
    if tracker is not None:
        tracker.add_node()

    # Khởi tạo danh sách steps nếu mode "all"
    steps = [state[:]] if (mode == "all" and state) else []

    # Kiểm tra đạt đích
    if check_goal(state, solution):
        if tracker is not None:
            tracker.goal_found()
        return steps if mode == "all" else state[:]

    # Dừng nếu hết limit
    if limit == 0:
        return steps if mode == "all" else None

    for col in range(8):
        if col not in state:
            child = state + [col]
            result = Recursive_DLS(child, solution, limit - 1, mode, tracker)

            if mode == "all":
                steps.extend(result)
            else:
                if result is not None:
                    return result

    return steps if mode == "all" else None
