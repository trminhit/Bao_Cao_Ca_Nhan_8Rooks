from typing import List, Tuple, Set, FrozenSet

World = Tuple[int, Tuple[int, ...]]   # hàng hiện tại, tuple các cột đã chiếm
Belief = FrozenSet[World]             # tập bất biến (frozenset) các world


#Sinh kq thực hiện hd trong word
def slide_outcomes_for_world(world: World, s: int, d, N: int) -> List[World]:
    """
    Sinh ra tất cả world có thể xảy ra khi thực hiện hành động (s, d) trên world hiện tại.
    - world: (row, occupied)
    - s: cột bắt đầu
    - d: hướng {None, 'L', 'R'}
    - N: kích thước bàn cờ
    """
    row, occ_t = world
    occupied = set(occ_t)
    outcomes = []

    if d is None:  
        if 0 <= s < N and s not in occupied:
            new_occ = tuple(sorted(occupied | {s}))
            outcomes.append((row + 1, new_occ))
        return outcomes

    if d == 'L':  # trượt sang trái
        for c in range(s, -1, -1):
            if c not in occupied:
                new_occ = tuple(sorted(occupied | {c}))
                outcomes.append((row + 1, new_occ))
        return outcomes

    if d == 'R':  # trượt sang phải
        for c in range(s, N):
            if c not in occupied:
                new_occ = tuple(sorted(occupied | {c}))
                outcomes.append((row + 1, new_occ))
        return outcomes

    return outcomes


# Sinh trạng thái niềm tin kế tiếp
def belief_successor(belief: Belief, s: int, d, N: int) -> Belief:
    """
    Cho 1 belief (tập world) và action (s, d), sinh ra belief mới
    = hợp của tất cả kết quả có thể từ mọi world.
    """
    succ_worlds = set()
    for world in belief:
        outs = slide_outcomes_for_world(world, s, d, N)
        for w in outs:
            succ_worlds.add(w)
    return frozenset(succ_worlds)



def AND_OR_BELIEF_SEARCH(N=8, initial_belief=None):
    """
    Hàm chính: tìm kế hoạch từ belief ban đầu.
    """
    if initial_belief is None:
        initial_belief = frozenset({(0, tuple())})  # bắt đầu: hàng 0, chưa chiếm cột nào
    else:
        initial_belief = frozenset(initial_belief)

    visited = set()  # để tránh lặp vòng
    return OR_SEARCH_BELIEF(initial_belief, tuple(), N, visited)


def OR_SEARCH_BELIEF(belief: Belief, path: Tuple, N: int, visited: Set[FrozenSet[World]]):
    # Kiểm tra goal: tất cả world trong belief đều đã đặt đủ N quân
    if all(world[0] == N for world in belief):
        return []  

    if belief in visited:
        return None
    visited.add(belief)

    # Thử tất cả hành động 
    for s in range(N):
        for d in (None, 'L', 'R'):
            succ = belief_successor(belief, s, d, N)
            if not succ:
                continue  # hành động này vô dụng

            # AND node: phải đảm bảo kế hoạch cho successor belief
            and_plan = AND_SEARCH_BELIEF([succ], path + (belief,), N, visited)
            if and_plan is not None:
                return [((s, d), and_plan)]

    # Không có hành động nào khả thi
    visited.remove(belief)
    return None


def AND_SEARCH_BELIEF(successor_beliefs: List[Belief], path: Tuple, N: int, visited: Set[FrozenSet[World]]):
    """
    Nút AND: phải đảm bảo tất cả belief con đều có kế hoạch đi đến goal.
    """
    combined = []
    for b in successor_beliefs:
        subplan = OR_SEARCH_BELIEF(b, path, N, visited)
        if subplan is None:
            return None
        combined.append(subplan)
    return combined
