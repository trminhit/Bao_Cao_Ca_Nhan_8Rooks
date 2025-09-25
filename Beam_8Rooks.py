import heapq

def H_match(state, solution):
    """Số quân đặt đúng vị trí so với solution (càng nhiều càng tốt)."""
    return sum(1 for i in range(len(state)) if state[i] == solution[i])

def BeamSearch(solution, beam_width ):
    """
    Thuật toán Beam Search
    - beam_width: số trạng thái tốt nhất giữ lại ở mỗi bước.
    """
    n = len(solution)
    # Trạng thái ban đầu: rỗng []
    beam = [([], 0)]   # (state, heuristic)
    path = {tuple([]): [[]]}  # Lưu đường đi tới mỗi state

    for row in range(n):
        candidates = []
        for state, heuristic_value in beam:
            for col in range(n):
                if col not in state:
                    next_state = state + [col]
                    h = H_match(next_state, solution)
                    candidates.append((next_state, h))

                    # Lưu lại đường đi
                    path[tuple(next_state)] = path[tuple(state)] + [next_state]

        if not candidates:
            return None

        # Chọn beam_width ứng viên tốt nhất theo H
        beam = heapq.nlargest(beam_width, candidates, key=lambda x: x[1])

        for state, heuristic_value in beam:
            if state == solution:
                return path[tuple(state)]

    return None
