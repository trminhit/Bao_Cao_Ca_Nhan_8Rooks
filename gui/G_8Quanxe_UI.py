import tkinter as tk
from tkinter import ttk
from algorithms import *
import random
import time
from PIL import Image, ImageTk

cell_s = 60

selected = None
Squares = {}
solution = [4,5,6,7,0,1,2,3]

GRADIENTS = {
    "purple_blue": ((147, 51, 234), (59, 130, 246)),
    "cyan_blue": ((6, 182, 212), (59, 130, 246)),
    "green_blue": ((74, 222, 128), (37, 99, 235)),
    "purple_pink": ((168, 85, 247), (236, 72, 153)),
    "pink_orange": ((236, 72, 153), (251, 146, 60)),
    "teal_lime": ((153, 246, 228), (217, 249, 157)),
    "red_yellow": ((254, 202, 202), (252, 165, 165), (254, 240, 138))
}

ALGORITHM_FUNCTIONS = {
    # Uninformed Search
    "BFS": lambda sol, mode="all": BFS_8Rooks.Find_Rooks_BFS(sol, mode),
    "DFS": lambda sol, mode="all": DFS_8Rooks.Find_Rooks_DFS(sol, mode),
    "DLS": lambda sol, mode="all": DLS_8Rooks.DepthLimitedSearch(sol, limit=8, mode=mode),
    "IDS": lambda sol, mode="all": IDS_8Rooks.IDS(sol, mode),
    "UCS": lambda sol, mode="all": UCS_8Rooks.UniformCostSearch(sol, mode)[1],
    # Informed Search
    "Greedy": lambda sol, mode="all": Greedy_8Rooks.GreedySearch(sol, mode),
    "A*": lambda sol, mode="all": AS_8Rooks.AStarSearch(sol, mode),
    # Local Search
    "Hill Climbing": lambda sol, mode="all": HillClimbing_8Rooks.HillClimbing(sol, mode),
    "Simulated Annealing": lambda sol, mode="all": 
        SimulatedAnnealing_8Rooks.SimulatedAnnealing(sol, T0=10.0, alpha=0.95, mode=mode),
    "Beam Search": lambda sol, mode="all": Beam_8Rooks.BeamSearch(sol, beam_width=4, mode=mode),
    "Genetic Algorithm": lambda sol, mode="all":
        Genetic_8Rooks.GeneticAlgorithm(sol, population_size=50, generations=500, mutation_rate=0.1, mode=mode),
}

ALGORITHM_GROUPS = {
    "Uninformed Search": {
        "gradient": "cyan_blue",
        "algorithms": ["BFS", "DFS", "DLS", "IDS", "UCS"]
    },
    "Informed Search": {
        "gradient": "green_blue",
        "algorithms": ["Greedy", "A*"]
    },
    "Local Search": {
        "gradient": "purple_pink",
        "algorithms": ["Hill Climbing", "Simulated Annealing", "Beam Search", "Genetic Algorithm"]
    },
    "Complex Environment": {
        "gradient": "pink_orange",
        "algorithms": ["Nondeterministic", "Conformant", "Contingency"]
    },
    "Complex Environment 2": {
        "gradient": "teal_lime",
        "algorithms": ["Genetic Algorithm", "Ant Colony Optimization", "Particle Swarm Optimization"]
    },
    "Machine Learning": {
        "gradient": "red_yellow",
        "algorithms": ["Q-Learning", "Neural Network Path", "Random Forest Path"]
    },
}

ALGORITHM_FUNCTIONS = {
    # Uninformed Search
    "BFS": lambda sol, mode="all": BFS_8Rooks.Find_Rooks_BFS(sol, mode),
    "DFS": lambda sol, mode="all": DFS_8Rooks.Find_Rooks_DFS(sol, mode),
    "DLS": lambda sol, mode="all": DLS_8Rooks.DepthLimitedSearch(sol, limit=8, mode=mode),
    "IDS": lambda sol, mode="all": IDS_8Rooks.IDS(sol, mode),
    "UCS": lambda sol, mode="all": UCS_8Rooks.UniformCostSearch(sol, mode)[1],
    # Informed Search
    "Greedy": lambda sol, mode="all": Greedy_8Rooks.GreedySearch(sol, mode),
    "A*": lambda sol, mode="all": AS_8Rooks.AStarSearch(sol, mode),
    # Local Search
    "Hill Climbing": lambda sol, mode="all": HillClimbing_8Rooks.HillClimbing(sol, mode),
    "Simulated Annealing": lambda sol, mode="all": 
        SimulatedAnnealing_8Rooks.SimulatedAnnealing(sol, T0=10.0, alpha=0.95, mode=mode),
    "Beam Search": lambda sol, mode="all": Beam_8Rooks.BeamSearch(sol, beam_width=4, mode=mode),
    "Genetic Algorithm": lambda sol, mode="all":
        Genetic_8Rooks.GeneticAlgorithm(sol, population_size=50, generations=500, mutation_rate=0.1, mode=mode),
}

def DrawBoard(canvas, x_start = 0, y_start = 0, rooks = None, rook_img=None):
    """ Vẽ bàn cờ """
    for r in range(8):
        for c in range(8):
            x1, y1 = x_start + c * cell_s, y_start + r * cell_s
            x2, y2 = x1 + cell_s, y1 + cell_s
            color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"
            square = canvas.create_rectangle(x1, y1, x2, y2, fill = color, outline = "")
            
    # Vẽ ký hiệu cột
    for c in range(8):
        x_center = x_start + c * cell_s + cell_s // 2
        canvas.create_text(x_center, y_start + 8 * cell_s + 15,
                           text=chr(ord('a') + c), font=("Helvetica", 10, "bold"))
        canvas.create_text(x_center, y_start - 15,
                           text=chr(ord('a') + c), font=("Helvetica", 10, "bold"))

    # Vẽ ký hiệu hàng 
    for r in range(8):
        y_center = y_start + r * cell_s + cell_s // 2
        canvas.create_text(x_start - 15, y_center,
                           text=str(8 - r), font=("Helvetica", 10, "bold"))
        canvas.create_text(x_start + 8 * cell_s + 15, y_center,
                           text=str(8 - r), font=("Helvetica", 10, "bold"))

        
    # Vẽ theo solution    
    if rooks and rook_img:
        for r, c in rooks:
            x_center = x_start + c * cell_s + cell_s // 2
            y_center = y_start + r * cell_s + cell_s // 2
            canvas.create_image(x_center, y_center, image = rook_img)
            
def WindowUI():
    """ Tạo cửa sổ, canvas, load hình ảnh quân hậu """
    root = tk.Tk()
    root.title("8 Rooks")
    y_offset = 80   
    x_offset = 380

    
    root.configure(bg="#f5f5f5")
    
    canvas_frame = tk.Frame(root, bg="#f5f5f5")
    canvas_frame.pack(side="right", fill="both", expand=True)
    
    canvas = tk.Canvas(canvas_frame, 
                     width=8 * cell_s * 2 + 540,
                     height=8 * cell_s + 180,
                     highlightthickness=0,
                     bg="#f5f5f5")
    canvas.pack()
    
    rook_img = ImageTk.PhotoImage(Image.open("assets/Rook_img.png").resize((cell_s, cell_s)))
    canvas.rook_img = rook_img
    
    Solution_btn = tk.Button(root, text="RANDOM SOLUTION", font=("Helvetica", 14, "bold"),
                        command=lambda: RandomSolution(canvas, rook_img))
    Solution_btn.place(x=x_offset + 8 * cell_s + 40, y=y_offset + 8 * cell_s + 90)
    algorithm_selector = AlgorithmSelector(root, canvas, rook_img)
    
    Draw_start_goal(canvas, rook_img)
    
    return root, canvas, rook_img

def RandomSolution(canvas, rook_img):
    global solution
    solution = random.sample(range(8), 8)   #Hoán vị của 0..7
    Draw_start_goal(canvas, rook_img)

class AlgorithmSelector:
    def __init__(self, parent, canvas, rook_img):
        self.parent = parent
        self.canvas = canvas
        self.rook_img = rook_img
        self.selected_algorithm = None
        self.selected_group = None
        self.is_running = False
        self.visualizer = RookVisualizer(canvas, rook_img, solution)
        
        # Container chính, tăng chiều rộng để căn giữa
        self.main_container = tk.Frame(parent, bg="#f5f5f5", relief="solid", bd=2)
        self.main_container.place(x=5, y=5, width=350, height=750)
        
        # Content frame
        content_frame = tk.Frame(self.main_container, bg="#f5f5f5")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Groups buttons
        self.groups_frame = tk.Frame(content_frame, bg="#f5f5f5")
        self.groups_frame.pack(fill="x", pady=(0, 15))
        self.create_group_buttons()
        
        # Separator
        separator = tk.Frame(content_frame, height=2, bg="#cccccc")
        separator.pack(fill="x", pady=15)
        
        # Algorithms buttons
        self.algorithms_frame = tk.Frame(content_frame, bg="#f5f5f5")
        self.algorithms_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Separator
        separator2 = tk.Frame(content_frame, height=2, bg="#cccccc")
        separator2.pack(fill="x", pady=15)
        
        # Start and Visual buttons
        self.create_buttons(content_frame)
    
    def create_group_buttons(self):
        self.group_buttons = {}
        group_names = list(ALGORITHM_GROUPS.keys())
        
        style = ttk.Style()
        style.configure("Group.TButton",
                       font=("Helvetica", 11, "bold"),
                       padding=(0, 15),
                       relief="flat")
        
        # Tạo bố cục động cho 6 nút (2 hàng x 3 cột)
        for row in range(3):
            row_frame = tk.Frame(self.groups_frame, bg="#f5f5f5")
            row_frame.pack(fill="x", pady=5)
            row_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="group")
            
            for col in range(2):
                index = row * 2 + col
                if index < len(group_names):
                    group_name = group_names[index]
                    btn = ttk.Button(row_frame,
                                    text=group_name,
                                    style="Group.TButton",
                                    cursor="hand2",
                                    command=lambda gn=group_name: self.select_group(gn))
                    btn.grid(row=0, column=col, padx=5, pady=5, sticky="ew")
                    self.group_buttons[group_name] = btn
    
    def select_group(self, group_name):
        self.selected_group = group_name
        self.selected_algorithm = None
        self.start_btn.configure(state="disabled")
        self.visual_btn.configure(state="disabled")
        self.show_algorithms(group_name)
    
    def show_algorithms(self, group_name):
        for widget in self.algorithms_frame.winfo_children():
            widget.destroy()
        
        algorithms = ALGORITHM_GROUPS[group_name]["algorithms"]
        for alg_name in algorithms:
            alg_btn = ttk.Button(self.algorithms_frame,
                                text=alg_name,
                                cursor="hand2",
                                command=lambda an=alg_name: self.select_algorithm(an))
            alg_btn.pack(fill="x", pady=3, padx=3)
            alg_btn.algorithm_name = alg_name
    
    def select_algorithm(self, algorithm_name):
        self.selected_algorithm = algorithm_name
        self.start_btn.configure(state="normal")
        self.visual_btn.configure(state="normal")
    
    def create_buttons(self, parent):
        style = ttk.Style()
        style.configure("Action.TButton",
                       font=("Helvetica", 13, "bold"),
                       padding=(15, 10))
        
        # Start button
        self.start_btn = ttk.Button(parent,
                                   text="START",
                                   style="Action.TButton",
                                   command=self.start_algorithm,
                                   state="disabled")
        self.start_btn.pack(fill="x", pady=5)
        
        # Visual button
        self.visual_btn = ttk.Button(parent,
                                    text="VISUAL",
                                    style="Action.TButton",
                                    command=self.visualize_algorithm,
                                    state="disabled")
        self.visual_btn.pack(fill="x", pady=5)
    
    def start_algorithm(self):
        if self.selected_algorithm and not self.is_running:
            self.is_running = True
            self.start_btn.configure(state="disabled")
            self.visual_btn.configure(state="disabled")
            
            # Hiển thị solution cuối cùng
            self.visualizer.show_solution(self.selected_algorithm)
            
            self.canvas.after(6000, self.stop_algorithm)
    
    def visualize_algorithm(self):
        if self.selected_algorithm and not self.is_running:
            self.is_running = True
            self.start_btn.configure(state="disabled")
            self.visual_btn.configure(state="disabled")
            
            # Hiển thị từng trạng thái
            self.visualizer.visualize(self.selected_algorithm)
            
            self.canvas.after(6000, self.stop_algorithm)
    
    def stop_algorithm(self):
        self.is_running = False
        self.start_btn.configure(state="normal" if self.selected_algorithm else "disabled")
        self.visual_btn.configure(state="normal" if self.selected_algorithm else "disabled")
        
def Draw_start_goal(canvas, rook_img):
    """ Vẽ bàn cờ bắt đầu và kết thúc """
    
    y_offset = 80
    x_offset = 380
    
    canvas.create_text(8 * cell_s + x_offset + 50, 20,
                      text="8 Rooks", font=("Helvetica", 18, "bold"), fill="black")
    
    # Bàn cờ trống (Start)
    DrawBoard(canvas, x_start=x_offset, y_start=y_offset)
    canvas.create_text(x_offset + 8 * cell_s // 2, y_offset + 8 * cell_s + 40,
                      text="Start", font=("Helvetica", 16, "bold"), fill="black")
    
    # Bàn cờ đích (Goal)
    rooks = [(r, solution[r]) for r in range(8)]
    DrawBoard(canvas, x_start=x_offset + 8 * cell_s + 80,
             y_start=y_offset, rooks=rooks, rook_img=rook_img)
    canvas.create_text(x_offset + 8 * cell_s + 40 + 8 * cell_s // 2 + 40,
                      y_offset + 8 * cell_s + 40,
                      text="Goal", font=("Helvetica", 16, "bold"), fill="black")


# def RookPlacing_BFS(canvas, rook_img, solution):
#     """Vẽ solution BFS từng quân xe một"""
#     canvas.delete("rook")
#     idx = 0  
#     def DrawNext():
#         nonlocal idx
#         if idx >= len(solution):
#             return  
        
#         r, c = idx, solution[idx]
#         x_center = 150 + c * cell_s + cell_s // 2
#         y_center = 80 + r * cell_s + cell_s // 2
#         canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

#         idx += 1
#         canvas.after(700, DrawNext)  
#     DrawNext()
    
# def RookPlacing_DFS(canvas, rook_img, solution):
#     """Vẽ solution DFS từng quân xe một"""
#     canvas.delete("rook")
#     idx = 0
#     def DrawNext():
#         nonlocal idx
#         if idx >= len(solution):
#             return

#         r, c = idx, solution[idx]
#         x_center = 150 + c * cell_s + cell_s // 2
#         y_center = 80 + r * cell_s + cell_s // 2
#         canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

#         idx += 1
#         canvas.after(700, DrawNext)
#     DrawNext()
        
# def RookPlacing_UCS(canvas, rook_img, solution):
#     """Vẽ solutiong UCS từng quân xe một"""
#     canvas.delete("rook")
    
#     cost, path = UCS_8Rooks.UniformCostSearch(solution)
#     idx = 0
#     def DrawNext():
#         nonlocal idx
#         if idx >= len(path):
#             return
        
#         r, c = idx, path[idx]
#         x_center = 150 + c * cell_s + cell_s // 2
#         y_center = 80 + r * cell_s + cell_s // 2
#         canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

#         idx += 1
#         canvas.after(700, DrawNext)
#     DrawNext()    
    
# def RookPlacing_DLS(canvas, rook_img, solution, limit=8):
#     """Vẽ solution DLS từng quân xe một"""
#     canvas.delete("rook")
#     path = DLS_8Rooks.DepthLimitedSearch(solution, limit)

#     if not path:
#         print("Không tìm thấy solution trong độ sâu=", limit)
#         return

#     idx = 0
#     def DrawNext():
#         nonlocal idx
#         if idx >= len(path):
#             return
        
#         r, c = idx, path[idx]
#         x_center = 150 + c * cell_s + cell_s // 2
#         y_center = 80 + r * cell_s + cell_s // 2
#         canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

#         idx += 1
#         canvas.after(700, DrawNext)
#     DrawNext()
    
# def RookPlacing_IDS(canvas, rook_img, solution):
#     """Vẽ solution IDS từng quân xe một"""
#     canvas.delete("rook")
#     path = IDS_8Rooks.IDS(solution)

#     if not path:
#         print("Không tìm thấy solution với IDS")
#         return

#     idx = 0
#     def DrawNext():
#         nonlocal idx
#         if idx >= len(path):
#             return
        
#         r, c = idx, path[idx]
#         x_center = 150 + c * cell_s + cell_s // 2
#         y_center = 80 + r * cell_s + cell_s // 2
#         canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

#         idx += 1
#         canvas.after(700, DrawNext)
#     DrawNext()

# def RookPlacing_Greedy(canvas, rook_img, solution):
#     """Vẽ solution Greedy từng quân xe một"""
#     canvas.delete("rook")
#     path = Greedy_8Rooks.GreedySearch(solution)  # chỉ nhận 1 giá trị path

#     if not path:
#         print("Không tìm thấy solution bằng Greedy")
#         return

#     idx = 0
#     def DrawNext():
#         nonlocal idx
#         if idx >= len(path):
#             return

#         r, c = idx, path[idx]
#         x_center = 150 + c * cell_s + cell_s // 2
#         y_center = 80 + r * cell_s + cell_s // 2
#         canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

#         idx += 1
#         canvas.after(700, DrawNext)
#     DrawNext()
    
# def RookPlacing_AStar(canvas, rook_img, solution):
#     """Vẽ solution A* từng quân xe một"""
    
#     canvas.delete("rook")
    
#     path = AS_8Rooks.AStarSearch(solution)

#     if not path:
#         print("Không tìm thấy solution bằng A*")
#         return

#     idx = 0
#     def DrawNext():
#         nonlocal idx
#         if idx >= len(path):
#             return

#         r, c = idx, path[idx]
#         x_center = 150 + c * cell_s + cell_s // 2
#         y_center = 80 + r * cell_s + cell_s // 2
#         canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

#         idx += 1
#         canvas.after(700, DrawNext)
#     DrawNext()
    
# def RookPlacing_HillClimbing(canvas, rook_img, solution):
#     """Vẽ solution Hill Climbing từng quân xe một"""
#     canvas.delete("rook")
#     path = HillClimbing_8Rooks.HillClimbing(solution)

#     if not path:
#         print("Không tìm thấy solution bằng Hill Climbing")
#         return

#     idx = 0
#     def DrawNext():
#         nonlocal idx
#         if idx >= len(path):
#             return

#         # lấy state hiện tại
#         state = path[idx]
#         canvas.delete("rook")  # xóa bước trước
#         for r, c in enumerate(state):
#             x_center = 150 + c * cell_s + cell_s // 2
#             y_center = 80 + r * cell_s + cell_s // 2
#             canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

#         idx += 1
#         canvas.after(700, DrawNext)

#     DrawNext()
    
# def RookPlacing_SA(canvas, rook_img, solution):
#     """Vẽ solution Simulated Annealing từng quân xe một"""
#     canvas.delete("rook")
#     path = SimulatedAnnealing_8Rooks.SimulatedAnnealing(solution, T0=10.0, alpha=0.95)

#     if not path:
#         print("Không tìm thấy solution bằng SA")
#         return

#     idx = 0
#     def DrawNext():
#         nonlocal idx
#         if idx >= len(path):
#             return

#         state = path[idx]
#         canvas.delete("rook")
#         for r, c in enumerate(state):
#             x_center = 150 + c * cell_s + cell_s // 2
#             y_center = 80 + r * cell_s + cell_s // 2
#             canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

#         idx += 1
#         canvas.after(700, DrawNext)

#     DrawNext()
    
# def RookPlacing_Beam(canvas, rook_img, solution, beam_width=4):
#     """Vẽ solution Beam Search từng quân xe một"""
#     canvas.delete("rook")
#     path = Beam_8Rooks.BeamSearch(solution, beam_width)

#     if not path:
#         print("Không tìm thấy solution bằng Beam Search")
#         return

#     idx = 0
#     def DrawNext():
#         nonlocal idx
#         if idx >= len(path):
#             return

#         # lấy state hiện tại
#         state = path[idx]
#         canvas.delete("rook")  # xóa bước trước
#         for r, c in enumerate(state):
#             x_center = 150 + c * cell_s + cell_s // 2
#             y_center = 80 + r * cell_s + cell_s // 2
#             canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

#         idx += 1
#         canvas.after(700, DrawNext)

#     DrawNext()
    
# def RookPlacing_GA(canvas, rook_img, solution, population_size=50, generations=500, mutation_rate=0.1):
#     canvas.delete("rook")
#     path = Genetic_8Rooks.GeneticAlgorithm(solution, population_size=population_size,
#                                            generations=generations, mutation_rate=mutation_rate)
#     if not path:
#         print("Không tìm thấy solution bằng GA")
#         return

#     # lấy trạng thái tốt nhất cuối cùng
#     final_state = path[-1]

#     idx = 0
#     def DrawNext():
#         nonlocal idx
#         if idx >= len(final_state):
#             return

#         r, c = idx, final_state[idx]
#         x_center = 150 + c * cell_s + cell_s // 2
#         y_center = 80 + r * cell_s + cell_s // 2
#         canvas.create_image(x_center, y_center, image=rook_img, tags="rook")
#         idx += 1
#         canvas.after(700, DrawNext)

#     DrawNext()
    
# def RookPlacing_ANDOR(canvas, rook_img, solution):
#     """Vẽ solution bằng AND-OR Search từng quân xe một"""
#     canvas.delete("rook")

#     # Gọi hàm AND_OR_SEARCH lấy kết quả
#     result = AndOr_8Rooks.AND_OR_SEARCH(N=8, goal=solution)

#     if not result:
#         print("Không tìm thấy solution bằng AND-OR")
#         return

#     # result sẽ là list cột [4,5,6,7,0,1,2,3]
#     path = result

#     idx = 0
#     def DrawNext():
#         nonlocal idx
#         if idx >= len(path):
#             return

#         r, c = idx, path[idx]
#         x_center = 150 + c * cell_s + cell_s // 2
#         y_center = 80 + r * cell_s + cell_s // 2
#         canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

#         idx += 1
#         canvas.after(700, DrawNext)

#     DrawNext()

class RookVisualizer:
    def __init__(self, canvas, rook_img, solution):
        self.canvas = canvas
        self.rook_img = rook_img
        self.solution = solution
        self.delay = 80  # Delay 50ms cho từng bước vẽ rook (nhanh)
        self.x_offset = 380  # Vị trí bàn cờ trung gian để vẽ animation
        self.y_offset = 80
    
    def show_solution(self, algorithm_name):
        """Vẽ giải pháp cuối cùng từng bước (mỗi rook một, delay 50ms)"""
        self.canvas.delete("rook")
        self.canvas.delete("debug")
        
        if algorithm_name not in ALGORITHM_FUNCTIONS:
            print(f"Algorithm {algorithm_name} not found!")
            self.canvas.create_text(self.x_offset + 4 * cell_s, 50,
                                    text=f"Algorithm {algorithm_name} not found!", 
                                    font=("Arial", 16), fill="red", tags="debug")
            return
            
        algo_func = ALGORITHM_FUNCTIONS[algorithm_name]
        
        try:
            result = algo_func(self.solution, mode="goal")
            print(f"Result from {algorithm_name} (goal): {result}")  # Debug
            final_state = result if isinstance(result, list) and result else None
        except Exception as e:
            print(f"Error running {algorithm_name}: {e}")
            self.canvas.create_text(self.x_offset + 4 * cell_s, 50,
                                    text=f"Error: {str(e)}", 
                                    font=("Arial", 16), fill="red", tags="debug")
            return
            
        if not final_state:
            return
        
        # Vẽ từng rook một trong final_state (mảng 1 chiều)
        self._animate_final_state(final_state, algorithm_name)
    
    def _animate_final_state(self, final_state, algorithm_name):
        """Animation vẽ từng rook trong giải pháp cuối (delay 50ms)"""
        idx = 0
        def place_next_rook():
            nonlocal idx
            if idx >= len(final_state):
                # Hoàn thành, hiển thị thông báo
                self.canvas.create_text(self.x_offset + 4 * cell_s, 50,
                                        text=f"Solution complete for {algorithm_name}", 
                                        font=("Arial", 16), fill="green", tags="debug")
                return
            
            # Vẽ rook hiện tại
            r, c = idx, final_state[idx]
            x_center = self.x_offset + c * cell_s + cell_s // 2
            y_center = self.y_offset + r * cell_s + cell_s // 2
            self.canvas.create_image(x_center, y_center, 
                                     image=self.rook_img, tags="rook")
            
            # Debug text
            self.canvas.create_text(self.x_offset + 4 * cell_s, 30,
                                    text=f"Placing rook {idx + 1}/8 at row {r}, col {c}", 
                                    font=("Arial", 12), fill="black", tags="debug")
            
            idx += 1
            # Delay 50ms cho bước tiếp theo
            self.canvas.after(self.delay, place_next_rook)
        
        place_next_rook()
    
    def visualize(self, algorithm_name):
        """Vẽ từng trạng thái, mỗi trạng thái vẽ từng rook (delay 50ms)"""
        self.canvas.delete("rook")
        self.canvas.delete("debug")
        
        if algorithm_name not in ALGORITHM_FUNCTIONS:
            print(f"Algorithm {algorithm_name} not found!")
            return
            
        algo_func = ALGORITHM_FUNCTIONS[algorithm_name]
        
        try:
            # Lấy tất cả states từ generator (mode="all")
            states_gen = algo_func(self.solution, mode="all")
            states = list(states_gen)  # Chuyển generator thành list để animation
            print(f"Total states from {algorithm_name}: {len(states)}")  # Debug
            print(f"First few states: {states[:5]}...")  # Debug
        except Exception as e:
            print(f"Error running {algorithm_name}: {e}")
            self.canvas.create_text(self.x_offset + 4 * cell_s, 50,
                                    text=f"Error: {str(e)}", 
                                    font=("Arial", 16), fill="red", tags="debug")
            return
            
        if not states:
            print(f"No states found for {algorithm_name}")
            self.canvas.create_text(self.x_offset + 4 * cell_s, 50,
                                    text=f"No states for {algorithm_name}", 
                                    font=("Arial", 16), fill="red", tags="debug")
            return
        
        # Bắt đầu animation từng trạng thái
        self._animate_states_step_by_step(states, algorithm_name, state_idx=0, rook_idx=0)
    
    def _animate_states_step_by_step(self, states, algorithm_name, state_idx=0, rook_idx=0):
        """Animation lồng nhau: từng trạng thái -> từng rook trong trạng thái (delay 50ms)"""
        if state_idx >= len(states):
            # Hoàn thành tất cả states
            self.canvas.create_text(self.x_offset + 4 * cell_s, 50,
                                    text=f"All states complete! ({algorithm_name})", 
                                    font=("Arial", 16), fill="green", tags="debug")
            return
        
        current_state = states[state_idx]
        
        # Nếu đã vẽ hết rooks trong state này, chuyển sang state tiếp theo
        if rook_idx >= len(current_state):
            # Xóa debug text cũ, chờ 200ms rồi chuyển state (để xem rõ state hiện tại)
            self.canvas.delete("debug")
            if state_idx + 1 < len(states):
                self.canvas.after(50, lambda: self._animate_states_step_by_step(states, algorithm_name, state_idx + 1, 0))
            return
        
        # Xóa rooks cũ trước khi vẽ state mới (chỉ lần đầu của state)
        if rook_idx == 0:
            self.canvas.delete("rook")
        
        # Vẽ rook hiện tại trong state hiện tại
        r, c = rook_idx, current_state[rook_idx]
        x_center = self.x_offset + c * cell_s + cell_s // 2
        y_center = self.y_offset + r * cell_s + cell_s // 2
        self.canvas.create_image(x_center, y_center, 
                                 image=self.rook_img, tags="rook")
        
        # Debug text cho state và rook hiện tại
        self.canvas.delete("debug")
        self.canvas.create_text(self.x_offset + 4 * cell_s, 30,
                                text=f"State {state_idx + 1}/{len(states)} | Rook {rook_idx + 1}/{len(current_state)}: row {r}, col {c} | State: {current_state}", 
                                font=("Arial", 10), fill="black", tags="debug")
        
        # Delay 50ms cho rook tiếp theo trong cùng state
        self.canvas.after(self.delay, lambda: self._animate_states_step_by_step(states, algorithm_name, state_idx, rook_idx + 1))