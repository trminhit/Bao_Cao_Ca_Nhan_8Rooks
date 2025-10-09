from engine.common_goal import check_goal, handle_goal_found
from engine.performance import PerformanceTracker

def Find_Rooks_BFS(solution, mode="all"):
    Queue = [[]]
    states = [] if mode == "all" else None
    tracker = PerformanceTracker("BFS")
    tracker.start()

    while Queue:
        col_select = Queue.pop(0)
        tracker.add_node()  # mỗi lần duyệt 1 node

        if mode == "all":
            states.append(col_select[:])

        if check_goal(col_select, solution):
            return handle_goal_found(mode, states, col_select, tracker)

        for col in range(8):
            if col not in col_select:
                Queue.append(col_select + [col])

    tracker.stop()
    tracker.print_stats()
    return (states, tracker.get_stats()) if mode == "all" else ([], tracker.get_stats())
