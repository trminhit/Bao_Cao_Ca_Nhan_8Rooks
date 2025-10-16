from engine.common_goal import check_goal, handle_goal_found
from engine.performance import PerformanceTracker

def Find_Rooks_DFS(solution, mode="all"):
    """DFS cho bài toán 8 Rooks"""
    Stack = [[]]
    states = [] if mode == "all" else None
    tracker = PerformanceTracker("DFS")
    tracker.start()

    while Stack:
        col_select = Stack.pop()
        tracker.add_node()  # đếm node

        if mode == "all":
            states.append(col_select[:])

        if check_goal(col_select, solution):
            return handle_goal_found(mode, states, col_select, tracker)

        #Sinh trạng thái kế tiếp
        for col in range(7, -1, -1):
            if col not in col_select:
                Stack.append(col_select + [col])

    #Không tìm thấy lời giải
    tracker.stop()
    tracker.print_stats()
    return (states, tracker.get_stats()) if mode == "all" else ([], tracker.get_stats())

