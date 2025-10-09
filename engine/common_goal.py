from engine.performance import PerformanceTracker

def check_goal(current_state, solution):
    """Kiểm tra trạng thái đạt đích"""
    return len(current_state) == len(solution) and current_state == solution

def handle_goal_found(mode, states, state, tracker):
    tracker.goal_found()
    tracker.stop()
    stats = tracker.get_stats()
    if mode == "all":
        return states, stats
    return state[:], stats
