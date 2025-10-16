import time

class PerformanceTracker:
    def __init__(self, algo_name="Algorithm"):
        self.algo_name = algo_name
        self.reset()

    def reset(self):
        self.start_time = None
        self.nodes_visited = 0
        self.solution_found = False

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.end_time = time.perf_counter()

    def add_node(self, count=1):
        """Gọi mỗi khi duyệt 1 node hoặc nhiều node."""
        self.nodes_visited += count

    def goal_found(self):
        """Đánh dấu đã tìm thấy lời giải."""
        self.solution_found = True

    def get_stats(self):
        # Nếu chưa stop, vẫn tính được elapsed time tạm thời
        end_time = getattr(self, "end_time", None) or time.perf_counter()
        elapsed = (end_time - self.start_time) if self.start_time else 0.0
        return {
            "algorithm": self.algo_name,
            "nodes_visited": self.nodes_visited,
            "elapsed_time": elapsed,
            "solution_found": self.solution_found
        }

    def print_stats(self):
        stats = self.get_stats()
        print(f"[{stats['algorithm']}] Nodes: {stats['nodes_visited']}, "
              f"Time: {stats['elapsed_time']*1000:.2f}ms, "
              f"Solution: {stats['solution_found']}")
