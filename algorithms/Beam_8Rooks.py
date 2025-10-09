import heapq
from engine.performance import PerformanceTracker

def H_match(state, solution):
    """Số quân đặt đúng vị trí so với solution (càng nhiều càng tốt)."""
    return sum(1 for i in range(len(state)) if state[i] == solution[i])

def BeamSearch(solution, beam_width, mode="goal"):
    """
    Thuật toán Beam Search cho 8 Rooks
    - beam_width: số trạng thái tốt nhất giữ lại ở mỗi bước
    """
    n = len(solution)
    beam = [([], 0)]   # (state, heuristic)
    path_map = {tuple([]): [[]]}  # Lưu đường đi tới mỗi state
    all_states = [] if mode == "all" else None

    tracker = PerformanceTracker("Beam Search")
    tracker.start()
    tracker.add_node()  # node gốc

    for row in range(n):
        candidates = []
        for state, heuristic_value in beam:
            for col in range(n):
                if col not in state:
                    next_state = state + [col]
                    h = H_match(next_state, solution)
                    candidates.append((next_state, h))

                    # Lưu đường đi
                    path_map[tuple(next_state)] = path_map[tuple(state)] + [next_state]

                    tracker.add_node()

                    if mode == "all":
                        all_states.append(next_state.copy())

                    if mode == "goal" and next_state == solution:
                        tracker.goal_found()
                        tracker.stop()
                        if mode == "all":
                            return (path_map[tuple(next_state)], tracker.get_stats())
                        else:
                            return (next_state, tracker.get_stats())

        if not candidates:
            tracker.stop()
            return (all_states if mode=="all" else [], tracker.get_stats())

        # Giữ lại beam_width ứng viên tốt nhất
        beam = heapq.nlargest(beam_width, candidates, key=lambda x: x[1])

    tracker.stop()
    return (all_states if mode=="all" else [], tracker.get_stats())
