import tkinter as tk
import BFS_8Rooks
import DFS_8Rooks
import UCS_8Rooks
import DLS_8Rooks
import IDS_8Rooks
import Greedy_8Rooks
import AS_8Rooks
import HillClimbing_8Rooks
import SimulatedAnnealing_8Rooks
import random
import time
from PIL import Image, ImageTk

cell_s = 60

selected = None
Squares = {}
solution = [4,5,6,7,0,1,2,3]

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
    
    canvas = tk.Canvas(root, 
                       width = 8 * cell_s * 2 + 350,
                       height = 8 * cell_s + 175,
                       highlightthickness=0,
                       bg="white")
    canvas.pack()
    
    #Load hình ảnh quân xe
    rook_img = ImageTk.PhotoImage(Image.open("Rook_img.png").resize((cell_s, cell_s)))
    canvas.rook_img = rook_img
    
    Solution_btn = tk.Button(root, text="RANDOM\nSOLUTION", font=("Helvetica", 14, "bold"),
                           command=lambda: RandomSolution(canvas, rook_img))
    Solution_btn.place(x=10, y=20)
    
    BFS_btn = tk.Button(root, text="Run BFS", font=("Helvetica", 14, "bold"),
                        command=lambda: RookPlacing_BFS(canvas, rook_img, solution))
    BFS_btn.place(x=10, y=90)
    
    DFS_btn = tk.Button(root, text="Run DFS", font=("Helvetica", 14, "bold"),
                        command=lambda: RookPlacing_DFS(canvas, rook_img, solution))
    DFS_btn.place(x=10, y=150)
    
    UCS_btn = tk.Button(root, text="Run UCS", font=("Helvetica", 14, "bold"),
                        command=lambda: RookPlacing_UCS(canvas, rook_img, solution))
    UCS_btn.place(x=10, y=210)
    
    DLS_btn = tk.Button(root, text="Run DLS", font=("Helvetica", 14, "bold"),
                        command=lambda: RookPlacing_DLS(canvas, rook_img, solution, limit=8))
    DLS_btn.place(x=10, y=270)
    
    IDS_btn = tk.Button(root, text="Run IDS", font=("Helvetica", 14, "bold"),
                    command=lambda: RookPlacing_IDS(canvas, rook_img, solution))
    IDS_btn.place(x=10, y=330)
    
    Greedy_btn = tk.Button(root, text="Run Greedy", font=("Helvetica", 14, "bold"),
                       command=lambda: RookPlacing_Greedy(canvas, rook_img, solution))
    Greedy_btn.place(x=10, y=390)
    
    AStar_btn = tk.Button(root, text="Run A*", font=("Helvetica", 14, "bold"),
                      command=lambda: RookPlacing_AStar(canvas, rook_img, solution))
    AStar_btn.place(x=10, y=450)
    
    HC_btn = tk.Button(root, text="Run Hill Climbing", font=("Helvetica", 14, "bold"),
                   command=lambda: RookPlacing_HillClimbing(canvas, rook_img, solution))
    HC_btn.place(x=10, y=510)
    
    SA_btn = tk.Button(root, text="Run SA", font=("Helvetica", 14, "bold"),
                   command=lambda: RookPlacing_SA(canvas, rook_img, solution))
    SA_btn.place(x=10, y=570)




    
    return root, canvas, rook_img

def RandomSolution(canvas, rook_img):
    global solution
    solution = random.sample(range(8), 8)   #Hoán vị của 0..7
    Draw_start_goal(canvas, rook_img)


def Draw_start_goal(canvas, rook_img):
    """ Vẽ bàn cờ bắt đầu và kết thúc """
    
    y_offset = 80   
    x_offset = 150   

    canvas.create_text(8 * cell_s + x_offset + 50, 30,   
                       text="8 Rooks", font=("Helvetica", 20, "bold"), fill="black")
    
    # Bàn cờ trống (Start)
    DrawBoard(canvas, x_start=x_offset, y_start=y_offset)
    canvas.create_text(x_offset + 8 * cell_s // 2, y_offset + 8 * cell_s + 50,
                       text="Begin", font=("Helvetica", 18, "bold"), fill = "black")
    
    # Bàn cờ đích (Goal)
    rooks = [(r, solution[r]) for r in range(8)]
    DrawBoard(canvas, x_start=x_offset + 8 * cell_s + 100, 
              y_start=y_offset, rooks=rooks, rook_img=rook_img)
    canvas.create_text(x_offset + 8 * cell_s + 40 + 8 * cell_s // 2 + 60,
                       y_offset + 8 * cell_s + 50,
                       text="Goal", font=("Helvetica", 18, "bold"), fill="black")

# def RookPlacing_BFS(canvas, rook_img, solution):
#     """ Đặt quân xe từng bước lên bàn cờ bằng BFS """
#     states = list(BFS_8Rooks.Find_Rooks_BFS(solution))  
#     idx = 0

#     def DrawStep():
#         nonlocal idx
#         if idx >= len(states):
#             return   
#         canvas.delete("rook")  
#         state = states[idx]
#         for r, c in state:
#             x_center = 150 + c * cell_s + cell_s // 2
#             y_center = 80 + r * cell_s + cell_s // 2
#             canvas.create_image(x_center, y_center, image=rook_img, tags="rook")  
#         idx += 1
#         canvas.after(10, DrawStep)  
#     DrawStep()   
def RookPlacing_BFS(canvas, rook_img, solution):
    """Vẽ solution BFS từng quân xe một"""
    canvas.delete("rook")
    idx = 0  
    def DrawNext():
        nonlocal idx
        if idx >= len(solution):
            return  
        
        r, c = idx, solution[idx]
        x_center = 150 + c * cell_s + cell_s // 2
        y_center = 80 + r * cell_s + cell_s // 2
        canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

        idx += 1
        canvas.after(700, DrawNext)  
    DrawNext()
    
# def RookPlacing_DFS(canvas, rook_img, solution):
#     """ Đặt quân xe từng bước lên bàn cờ bằng DFS """
#     states = list(DFS_8Rooks.Find_Rooks_DFS(solution))
#     idx = 0
#     def DrawStep():
#         nonlocal idx
#         if idx >= len(states):
#             return
#         canvas.delete("rook")  
#         state = states[idx]
#         for r, c in state:
#             x_center = 150 + c * cell_s + cell_s // 2
#             y_center = 80 + r * cell_s + cell_s // 2
#             canvas.create_image(x_center, y_center, image=rook_img, tags="rook")
#         idx += 1
#         canvas.after(10, DrawStep)  
#     DrawStep()
def RookPlacing_DFS(canvas, rook_img, solution):
    """Vẽ solution DFS từng quân xe một"""
    canvas.delete("rook")
    idx = 0
    def DrawNext():
        nonlocal idx
        if idx >= len(solution):
            return

        r, c = idx, solution[idx]
        x_center = 150 + c * cell_s + cell_s // 2
        y_center = 80 + r * cell_s + cell_s // 2
        canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

        idx += 1
        canvas.after(700, DrawNext)
    DrawNext()
        
def RookPlacing_UCS(canvas, rook_img, solution):
    """Vẽ solutiong UCS từng quân xe một"""
    canvas.delete("rook")
    
    cost, path = UCS_8Rooks.UniformCostSearch(solution)
    idx = 0
    def DrawNext():
        nonlocal idx
        if idx >= len(path):
            return
        
        r, c = idx, path[idx]
        x_center = 150 + c * cell_s + cell_s // 2
        y_center = 80 + r * cell_s + cell_s // 2
        canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

        idx += 1
        canvas.after(700, DrawNext)
    DrawNext()    
    
def RookPlacing_DLS(canvas, rook_img, solution, limit=8):
    """Vẽ solution DLS từng quân xe một"""
    canvas.delete("rook")
    path = DLS_8Rooks.DepthLimitedSearch(solution, limit)

    if not path:
        print("Không tìm thấy solution trong độ sâu=", limit)
        return

    idx = 0
    def DrawNext():
        nonlocal idx
        if idx >= len(path):
            return
        
        r, c = idx, path[idx]
        x_center = 150 + c * cell_s + cell_s // 2
        y_center = 80 + r * cell_s + cell_s // 2
        canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

        idx += 1
        canvas.after(700, DrawNext)
    DrawNext()
    
def RookPlacing_IDS(canvas, rook_img, solution):
    """Vẽ solution IDS từng quân xe một"""
    canvas.delete("rook")
    path = IDS_8Rooks.IDS(solution)

    if not path:
        print("Không tìm thấy solution với IDS")
        return

    idx = 0
    def DrawNext():
        nonlocal idx
        if idx >= len(path):
            return
        
        r, c = idx, path[idx]
        x_center = 150 + c * cell_s + cell_s // 2
        y_center = 80 + r * cell_s + cell_s // 2
        canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

        idx += 1
        canvas.after(700, DrawNext)
    DrawNext()

def RookPlacing_Greedy(canvas, rook_img, solution):
    """Vẽ solution Greedy từng quân xe một"""
    canvas.delete("rook")
    path = Greedy_8Rooks.GreedySearch(solution)  # chỉ nhận 1 giá trị path

    if not path:
        print("Không tìm thấy solution bằng Greedy")
        return

    idx = 0
    def DrawNext():
        nonlocal idx
        if idx >= len(path):
            return

        r, c = idx, path[idx]
        x_center = 150 + c * cell_s + cell_s // 2
        y_center = 80 + r * cell_s + cell_s // 2
        canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

        idx += 1
        canvas.after(700, DrawNext)
    DrawNext()
    
def RookPlacing_AStar(canvas, rook_img, solution):
    """Vẽ solution A* từng quân xe một"""
    
    canvas.delete("rook")
    
    path = AS_8Rooks.AStarSearch(solution)

    if not path:
        print("Không tìm thấy solution bằng A*")
        return

    idx = 0
    def DrawNext():
        nonlocal idx
        if idx >= len(path):
            return

        r, c = idx, path[idx]
        x_center = 150 + c * cell_s + cell_s // 2
        y_center = 80 + r * cell_s + cell_s // 2
        canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

        idx += 1
        canvas.after(700, DrawNext)
    DrawNext()
    
def RookPlacing_HillClimbing(canvas, rook_img, solution):
    """Vẽ solution Hill Climbing từng quân xe một"""
    canvas.delete("rook")
    path = HillClimbing_8Rooks.HillClimbing(solution)

    if not path:
        print("Không tìm thấy solution bằng Hill Climbing")
        return

    idx = 0
    def DrawNext():
        nonlocal idx
        if idx >= len(path):
            return

        # lấy state hiện tại
        state = path[idx]
        canvas.delete("rook")  # xóa bước trước
        for r, c in enumerate(state):
            x_center = 150 + c * cell_s + cell_s // 2
            y_center = 80 + r * cell_s + cell_s // 2
            canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

        idx += 1
        canvas.after(700, DrawNext)

    DrawNext()
    
def RookPlacing_SA(canvas, rook_img, solution):
    """Vẽ solution Simulated Annealing từng quân xe một"""
    canvas.delete("rook")
    path = SimulatedAnnealing_8Rooks.SimulatedAnnealing(solution, T0=10.0, alpha=0.95)

    if not path:
        print("Không tìm thấy solution bằng SA")
        return

    idx = 0
    def DrawNext():
        nonlocal idx
        if idx >= len(path):
            return

        state = path[idx]
        canvas.delete("rook")
        for r, c in enumerate(state):
            x_center = 150 + c * cell_s + cell_s // 2
            y_center = 80 + r * cell_s + cell_s // 2
            canvas.create_image(x_center, y_center, image=rook_img, tags="rook")

        idx += 1
        canvas.after(700, DrawNext)

    DrawNext()
