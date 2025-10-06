import heapq

def H_match(state, solution):
    """Số quân đặt đúng vị trí so với solution (càng nhiều càng tốt)."""
    return sum(1 for i in range(len(state)) if state[i] == solution[i])

def BeamSearch(solution, beam_width, mode="goal"):
    """
    Thuật toán Beam Search
    - beam_width: số trạng thái tốt nhất giữ lại ở mỗi bước
    """
    n = len(solution)
    beam = [([], 0)]   # (state, heuristic)
    path = {tuple([]): [[]]}  # Lưu đường đi tới mỗi state
    all_states = [] if mode == "all" else None

    for row in range(n):
        candidates = []
        for state, heuristic_value in beam:
            for col in range(n):
                if col not in state:
                    next_state = state + [col]
                    h = H_match(next_state, solution)
                    candidates.append((next_state, h))
                    # Lưu đường đi
                    path[tuple(next_state)] = path[tuple(state)] + [next_state]
                    
                    if mode == "all":
                        all_states.append(next_state.copy())

                    if mode == "goal" and next_state == solution:
                        return path[tuple(next_state)] if mode == "all" else next_state

        if not candidates:
            return None

        # Giữ lại beam_width ứng viên tốt nhất
        beam = heapq.nlargest(beam_width, candidates, key=lambda x: x[1])

    if mode == "all":
        return all_states
    return None
