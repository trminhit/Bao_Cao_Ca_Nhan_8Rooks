import pygame
import sys
import time
import random
from PIL import Image
from algorithms import *
from gui.renderer import Renderer

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
CELL_SIZE = 60
BOARD_SIZE = 8
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE
BOARD_OFFSET_X = 400
BOARD_OFFSET_Y = 80
SMALL_CELL_SIZE = 37

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 140, 0)
CYAN = (0, 200, 200)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)

class RooksGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("8 Rooks Pathfinding - Algorithm Selection")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('segoeui', 20)
        self.title_font = pygame.font.SysFont('segoeui', 28, bold=True)
        self.small_font = pygame.font.SysFont('segoeui', 16)
        
        rook_img = Image.open("assets/Rook_img.png").resize((SMALL_CELL_SIZE, SMALL_CELL_SIZE))
        self.rook_img = pygame.image.fromstring(rook_img.tobytes(), rook_img.size, rook_img.mode)
        
        self.history = []
        self.solution = random.sample(range(8), 8)
        
        self.BOARD_SIZE = BOARD_SIZE
        self.BOARD_WIDTH = BOARD_WIDTH
        self.BOARD_HEIGHT = BOARD_HEIGHT
        self.CELL_SIZE = CELL_SIZE
        self.BOARD_OFFSET_X = BOARD_OFFSET_X
        self.BOARD_OFFSET_Y = BOARD_OFFSET_Y
        
        self.renderer = Renderer(self.screen, self, self.rook_img)
        
        self.selected_group = 0
        self.selected_algorithm = 0
        self.is_running = False
        self.stats = {"nodes_visited": 0, "path_length": 0, "time": 0}
        self._perf_snapshot = None #lưu perf dict trả về từ thuật toán

        
        self.start_time = 0
        self.visualizer = RookVisualizer(self.screen, self.rook_img, self.solution, self)
        
        self.animation_active = False
        self.animation_type = None
        self.animation_data = None
        self.animation_idx = 0
        self.last_animation_time = 0
        self.current_rooks = []
        
        self.algorithms = {
            "BFS": lambda sol, mode="all": BFS_8Rooks.Find_Rooks_BFS(sol, mode),
            "DFS": lambda sol, mode="all": DFS_8Rooks.Find_Rooks_DFS(sol, mode),
            "DLS": lambda sol, mode="all": DLS_8Rooks.DepthLimitedSearch(sol, limit=8, mode=mode),
            "IDS": lambda sol, mode="all": IDS_8Rooks.IDS(sol, mode),
            "UCS": lambda sol, mode="all": UCS_8Rooks.UniformCostSearch(sol, mode),
            "Greedy": lambda sol, mode="all": Greedy_8Rooks.GreedySearch(sol, mode),
            "A*": lambda sol, mode="all": AS_8Rooks.AStarSearch(sol, mode),
            "Hill Climbing": lambda sol, mode="all": HillClimbing_8Rooks.HillClimbing(sol, mode),
            "Simulated Annealing": lambda sol, mode="all": SimulatedAnnealing_8Rooks.SimulatedAnnealing(sol, T0=10.0, alpha=0.95, mode=mode),
            "Beam Search": lambda sol, mode="all": Beam_8Rooks.BeamSearch(sol, beam_width=4, mode=mode),
            "Genetic Algorithm": lambda sol, mode="all": Genetic_8Rooks.GeneticAlgorithm(sol, population_size=50, generations=500, mutation_rate=0.1, mode=mode),
            "Nondeterministic": lambda sol, mode="all": AndOr_8Rooks.AND_OR_SEARCH(N=8, goal=sol, mode=mode),
            "Unobservable Search": lambda sol, mode="all": Unobservable_8Rooks.Find_Rooks_DFS_Belief(sol, mode=mode),
            "Partial Observable": lambda sol, mode="all": PartialObservable.Find_Rooks_DFS_Belief(sol, mode=mode),
            "Backtracking": lambda sol, mode="all": Backtracking_8Rooks.Backtracking(sol, mode),
            "Forward Checking": lambda sol, mode="all": ForwardChecking_8Rooks.ForwardChecking(sol, mode),
            "Arc Consistency Algorithm 3": lambda sol, mode="all": AC3_8Rooks.AC3(sol, mode),
        }

    def handle_click(self, pos):
        for i in range(len(self.renderer.algorithm_groups)):
            if self.renderer.get_group_button_rect(i).collidepoint(pos):
                self.selected_group = i
                self.selected_algorithm = 0
                self.draw_frame()
                return

        current_group = self.renderer.algorithm_groups[self.selected_group]
        for i, alg in enumerate(current_group["algorithms"]):
            if self.renderer.get_algorithm_button_rect(self.selected_group, i).collidepoint(pos):
                self.selected_algorithm = i
                self.draw_frame()
                return

        actions = ["start", "visualize", "stop", "random_solution"]
        for i, action in enumerate(actions):
            if self.renderer.get_control_button_rect(i).collidepoint(pos):
                if action == "start":
                    self.start_algorithm()
                elif action == "visualize":
                    self.visualize_algorithm()
                elif action == "stop":
                    self.stop_animation()
                elif action == "random_solution" and not self.is_running:
                    self.random_solution()
                return

    def get_current_algorithm_name(self):
        group = self.renderer.algorithm_groups[self.selected_group]
        alg = group["algorithms"][self.selected_algorithm]
        return alg["name"]

    def stop_animation(self):
        """Dừng animation và cập nhật stats dựa trên PerformanceTracker nếu có."""
        if self.animation_active:
            perf = self._perf_snapshot or {}

            alg_name = self.get_current_algorithm_name()

            # --- Tính nodes đã hiển thị ---
            nodes_shown = 0
            if "Unobservable" in alg_name or "Partial Observable" in alg_name:
                for idx, frame in enumerate(self.animation_data[:self.animation_idx]):
                    if isinstance(frame, list) and frame and isinstance(frame[0], list):
                        nodes_shown += len(frame)
                    else:
                        nodes_shown += 1
                if self.animation_idx < len(self.animation_data):
                    frame = self.animation_data[self.animation_idx]
                    if isinstance(frame, list) and frame and isinstance(frame[0], list):
                        nodes_shown += getattr(self, "sub_state_idx", 0)
                    else:
                        nodes_shown += 1
            else:
                nodes_shown = self.animation_idx

            # --- Cập nhật stats ---
            self.stats["nodes_visited"] = nodes_shown
            total_time = perf.get("elapsed_time", 0.0) * 1000 * 50
            if perf.get("nodes_visited", 0) > 0:
                self.stats["time"] = total_time * nodes_shown / perf.get("nodes_visited", 1)
            else:
                self.stats["time"] = total_time
            self.stats["path_length"] = len(self.current_rooks)

            # Nếu animation chưa tìm ra giải thì path_length = 0
            if not perf.get("solution_found", False):
                self.stats["path_length"] = 0

            # --- Ghi history ---
            if self.stats["nodes_visited"] > 0:
                self.history.insert(0, {
                    "name": alg_name,
                    "nodes": self.stats["nodes_visited"],
                    "length": self.stats["path_length"],
                    "time": f"{self.stats['time']:.0f}ms"
                })

            # --- Dừng animation ---
            self.animation_active = False
            self.is_running = False
            self.draw_frame()

    def start_algorithm(self):
        """Start selected algorithm, chế độ 'start' vẽ incremental lời giải cuối cùng."""
        self.animation_type = 'start'

        self.animation_active = False
        self.is_running = False
        self.current_rooks = []
        self.draw_frame()

        self.is_running = True
        self.start_time = time.time()
        self.stats = {"nodes_visited": 0, "path_length": 0, "time": 0}
        self._perf_snapshot = {}
        self.animation_data = []
        self.animation_idx = 0

        alg_name = self.get_current_algorithm_name()
        if alg_name not in self.algorithms:
            print(f"⚠ Algorithm {alg_name} not implemented!")
            self.is_running = False
            return

        algo_func = self.algorithms[alg_name]
        try:
            result = algo_func(self.solution, mode="goal")

            frames = []
            final_perf = {}

            if hasattr(result, '__next__'):  # generator
                try:
                    while True:
                        belief, perf = next(result)
                        final_perf = perf
                        # tạo incremental frames từ belief hiện tại
                        frames.append(list(belief))  # copy list
                except StopIteration:
                    pass
            else:  # non-generator
                final_belief, final_perf = result
                final_belief = final_belief or []
                for i in range(1, len(final_belief)+1):
                    frames.append(final_belief[:i])

            self.animation_data = frames or [[]]
            self._perf_snapshot = final_perf.copy() if isinstance(final_perf, dict) else {}
            self.stats["nodes_visited"] = self._perf_snapshot.get("nodes_visited", len(self.animation_data))
            self.stats["time"] = self._perf_snapshot.get("elapsed_time", 0) * 1000 *50
            self.stats["path_length"] = len(frames[-1]) if frames else 0

            self.animation_active = True
            self.animation_type = 'start'
            self.animation_idx = 0
            self.last_animation_time = pygame.time.get_ticks()

        except Exception as e:
            print(f"Error running {alg_name}: {e}")
            import traceback
            traceback.print_exc()
            self.is_running = False

    def visualize_algorithm(self):
        """Visualize the selected algorithm, xóa quân xe cũ.
        Chế độ 'visualize' thu thập tất cả các belief/state để animate toàn bộ quá trình."""
        self.animation_type = 'visual'
        self.animation_active = False
        self.is_running = False
        self.current_rooks = []
        self.draw_frame()

        self.is_running = True
        self.start_time = time.time()
        self.stats = {"nodes_visited": 0, "path_length": 0, "time": 0}
        self._perf_snapshot = None
        self.animation_gen = None
        self.animation_data = None
        self.animation_idx = 0
        alg_name = self.get_current_algorithm_name()

        if alg_name in self.algorithms:
            algo_func = self.algorithms[alg_name]
            try:
                result = algo_func(self.solution, mode="all")
                if hasattr(result, '__next__'):
                    all_beliefs = []
                    last_perf = {}
                    # result is a generator yielding (belief, perf)
                    try:
                        while True:
                            belief, perf = next(result)
                            # belief = list of possible states
                            # Chỉ lấy state đầu tiên để visualize
                            if belief and len(belief) > 0:
                                first_state = belief[0]
                                all_beliefs.append(first_state if first_state else [])
                            else:
                                all_beliefs.append([])
                            last_perf = perf
                    except StopIteration:
                        pass

                    self.animation_data = all_beliefs
                    self._perf_snapshot = last_perf.copy() if isinstance(last_perf, dict) else {}
                    self.stats["nodes_visited"] = self._perf_snapshot.get("nodes_visited", len(all_beliefs))
                    self.stats["time"] = self._perf_snapshot.get("elapsed_time", 0) * 1000 *50

                    self.animation_active = True
                    self.animation_type = 'visualize'
                    self.animation_idx = 0
                    self.last_animation_time = pygame.time.get_ticks()

                else:
                    # non-generator path: could be (states, perf) or states
                    if isinstance(result, tuple):
                        states, perf = result
                    else:
                        states, perf = result, {}

                    self.animation_data = states if isinstance(states, list) else []
                    self._perf_snapshot = perf.copy() if isinstance(perf, dict) else {}
                    self.stats["nodes_visited"] = self._perf_snapshot.get("nodes_visited", len(self.animation_data))
                    self.stats["time"] = self._perf_snapshot.get("elapsed_time", 0) * 1000 *50

                    self.animation_active = True
                    self.animation_type = 'visualize'
                    self.animation_idx = 0
                    self.last_animation_time = pygame.time.get_ticks()

            except Exception as e:
                print(f"Error running {alg_name}: {e}")
                import traceback
                traceback.print_exc()
                self.is_running = False
        else:
            print(f"!!! Algorithm {alg_name} not implemented!")
            self.is_running = False

    def random_solution(self):
        self.solution = random.sample(range(8), 8)
        self.history = []
        self.stats = {"nodes_visited": 0, "path_length": 0, "time": 0}
        self.animation_active = False
        self.is_running = False
        self.current_rooks = []
        self.draw_frame()

    def update_animation(self):
        if not self.animation_active or not self.animation_data:
            return

        current_time = pygame.time.get_ticks()
        delay = 200 if self.animation_type == 'start' else 80
        if current_time - self.last_animation_time < delay:
            return
        self.last_animation_time = current_time

        def normalize_state(state):
            """Chuyển state (int, list hoặc None) thành list (row, col) chuẩn."""
            if not state:
                return []
            result = []
            for r, col in enumerate(state):
                if r >= 8:
                    break
                if col is None:
                    continue
                if isinstance(col, int) and 0 <= col < 8:
                    result.append((r, col))
                elif isinstance(col, list) and col and 0 <= col[0] < 8:
                    result.append((r, col[0]))
            return result

        alg_name = self.get_current_algorithm_name()
        if not hasattr(self, 'sub_state_idx'):
            self.sub_state_idx = 0

        # --- Kiểm tra kết thúc animation ---
        if self.animation_idx >= len(self.animation_data):
            self.animation_active = False
            self.is_running = False
            final_frame = self.animation_data[-1] if self.animation_data else []
            self.current_rooks = normalize_state(
                final_frame[-1] if ("Unobservable" in alg_name or "Partial Observable" in alg_name) and isinstance(final_frame, list) and final_frame and isinstance(final_frame[0], list) else final_frame
            )
            if self._perf_snapshot:
                self.stats["nodes_visited"] = self._perf_snapshot.get("nodes_visited", len(self.animation_data))
                self.stats["time"] = self._perf_snapshot.get("elapsed_time", 0) * 1000 *50
            self.stats["path_length"] = len(self.current_rooks)

            self.history.insert(0, {
                "name": alg_name,
                "nodes": self.stats["nodes_visited"],
                "length": self.stats["path_length"],
                "time": f"{self.stats['time']:.0f}ms"
            })
            return

        current_frame = self.animation_data[self.animation_idx]

        # --- Partial / Unobservable ---
        if "Unobservable" in alg_name or "Partial Observable" in alg_name:
            if self.animation_type == "start":
                # Lấy state cuối cùng trong frame hiện tại
                state = current_frame[-1] if isinstance(current_frame, list) and current_frame and isinstance(current_frame[0], list) else current_frame
                self.current_rooks = normalize_state(state)
                self.animation_idx += 1
                self.sub_state_idx = 0
            else:  # visualize
                if not current_frame:
                    self.animation_idx += 1
                    self.sub_state_idx = 0
                    return

                if self.sub_state_idx >= len(current_frame):
                    self.sub_state_idx = 0
                    self.animation_idx += 1
                    return

                sub_state = current_frame[self.sub_state_idx]
                if isinstance(sub_state, int):
                    sub_state = [sub_state]

                self.current_rooks = normalize_state(sub_state)
                self.sub_state_idx += 1

        # --- Start / Goal hoặc các thuật toán khác ---
        else:
            state = current_frame
            if isinstance(state, list) and len(state) == 1 and isinstance(state[0], list):
                state = state[0]
            self.current_rooks = normalize_state(state)
            self.animation_idx += 1

        # --- Cập nhật stats ---
        if self._perf_snapshot:
            total_nodes = self._perf_snapshot.get("nodes_visited", len(self.animation_data))
            total_time = self._perf_snapshot.get("elapsed_time", 0) * 1000 * 50

            if "Unobservable" in alg_name or "Partial Observable" in alg_name:
                nodes_shown = 0
                for idx, frame in enumerate(self.animation_data[:self.animation_idx]):
                    if isinstance(frame, list) and frame and isinstance(frame[0], list):
                        nodes_shown += len(frame)
                    else:
                        nodes_shown += 1
                if self.animation_idx < len(self.animation_data):
                    frame = self.animation_data[self.animation_idx]
                    if isinstance(frame, list) and frame and isinstance(frame[0], list):
                        nodes_shown += self.sub_state_idx
                self.stats["nodes_visited"] = nodes_shown
            else:
                progress = (self.animation_idx + 1) / len(self.animation_data)
                self.stats["nodes_visited"] = int(total_nodes * progress)

            progress = min(1.0, self.stats["nodes_visited"] / total_nodes) if total_nodes > 0 else 0
            self.stats["time"] = total_time * progress 
            self.stats["path_length"] = len(self.current_rooks)
    
    def draw_frame(self):
        self.screen.fill(WHITE)
        self.renderer.draw_all()
        if self.current_rooks:
            self.visualizer.draw_animation_board(self.current_rooks, clear_background=False)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)

            self.update_animation()
            self.draw_frame()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

class RookVisualizer:
    def __init__(self, screen, rook_img, solution, game):
        self.screen = screen
        self.rook_img = rook_img
        self.solution = solution
        self.game = game
        self.x_offset = BOARD_OFFSET_X
        self.y_offset = BOARD_OFFSET_Y
        self.cell_size = SMALL_CELL_SIZE

    def draw_animation_board(self, rooks=None, clear_background=True):
        if clear_background:
            board_rect = pygame.Rect(self.x_offset, self.y_offset, 8 * self.cell_size, 8 * self.cell_size)
            pygame.draw.rect(self.screen, WHITE, board_rect)

        for r in range(8):
            for c in range(8):
                x1, y1 = self.x_offset + c * self.cell_size, self.y_offset + r * self.cell_size
                color = (240, 217, 181) if (r + c) % 2 == 0 else (181, 136, 99)
                pygame.draw.rect(self.screen, color, (x1, y1, self.cell_size, self.cell_size))

        if clear_background:
            for c in range(8):
                x_center = self.x_offset + c * self.cell_size + self.cell_size // 2
                text = self.game.small_font.render(chr(ord('a') + c), True, BLACK)
                text_rect = text.get_rect(center=(x_center, self.y_offset + 8 * self.cell_size + 10))
                self.screen.blit(text, text_rect)
                text_rect = text.get_rect(center=(x_center, self.y_offset - 10))
                self.screen.blit(text, text_rect)

            for r in range(8):
                y_center = self.y_offset + r * self.cell_size + self.cell_size // 2
                text = self.game.small_font.render(str(8 - r), True, BLACK)
                text_rect = text.get_rect(center=(self.x_offset - 10, y_center))
                self.screen.blit(text, text_rect)
                text_rect = text.get_rect(center=(self.x_offset + 8 * self.cell_size + 10, y_center))
                self.screen.blit(text, text_rect)

        if rooks:
            for r, c in rooks:
                if isinstance(c, list) and c:  # phòng trường hợp chưa normalize
                    c = c[0]
                x_center = self.x_offset + c * self.cell_size + self.cell_size // 2
                y_center = self.y_offset + r * self.cell_size + self.cell_size // 2
                rook_rect = self.rook_img.get_rect(center=(x_center, y_center))
                self.screen.blit(self.rook_img, rook_rect)