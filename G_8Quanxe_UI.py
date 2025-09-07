import tkinter as tk
import BFS_8Rooks
import time
from PIL import Image, ImageTk

cell_s = 60

selected = None
Squares = {}

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
        # Bên dưới: a → h
        canvas.create_text(x_center, y_start + 8 * cell_s + 15, text=chr(ord('a') + c), font=("Arial", 10, "bold"))
        # Bên trên: h → a
        canvas.create_text(x_center, y_start - 15, text=chr(ord('h') - c), font=("Arial", 10, "bold"))

    # Vẽ ký hiệu hàng 
    for r in range(8): 
        y_center = y_start + r * cell_s + cell_s // 2
        # Bên trái: 8 -> 1
        canvas.create_text(x_start - 15, y_center, text=str(8 - r), font=("Arial", 10, "bold"))
        # Bên phải: 1 → 8
        canvas.create_text(x_start + 8 * cell_s + 15, y_center, text=str(r + 1), font=("Arial", 10, "bold"))
        
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
    
    BFS_btn = tk.Button(root, text="Run BFS", font=("Arial", 14, "bold"),
                        command=lambda: RookPlacing(canvas, rook_img))
    BFS_btn.place(x=10, y=90)
    
    return root, canvas, rook_img

def Draw_start_goal(canvas, rook_img):
    """ Vẽ bàn cờ bắt đầu và kết thúc """
    
    y_offset = 80   
    x_offset = 150   

    canvas.create_text(8 * cell_s + x_offset + 50, 30,   
                       text="8 Rooks", font=("Arial", 20, "bold"), fill="black")
    
    # Bàn cờ trống (Start)
    DrawBoard(canvas, x_start=x_offset, y_start=y_offset)
    canvas.create_text(x_offset + 8 * cell_s // 2, y_offset + 8 * cell_s + 50,
                       text="Begin", font=("Arial", 18, "bold"), fill = "black")
    
    # Bàn cờ đích (Goal)
    rooks = BFS_8Rooks.Find_Rooks()
    DrawBoard(canvas, x_start=x_offset + 8 * cell_s + 100, 
              y_start=y_offset, rooks=rooks, rook_img=rook_img)
    canvas.create_text(x_offset + 8 * cell_s + 40 + 8 * cell_s // 2 + 60,
                       y_offset + 8 * cell_s + 50,
                       text="Goal", font=("Arial", 18, "bold"), fill="black")

def RookPlacing(canvas, rook_img):
    """ Đặt quân xe từng bước lên bàn cờ trống """
    solution = BFS_8Rooks.Find_Rooks()
    
    def PlaceStep(i):
        if i < len(solution):
            r, c = solution[i]
            x_center = 150 + c * cell_s + cell_s // 2
            y_center = 80 + r * cell_s + cell_s // 2
            canvas.create_image(x_center, y_center, image=rook_img)
         
            #widget.after(delay_ms, callback), delay sau do callback sau khoang tg do
            # Gọi lại tiếp bước kế sau 500ms
            canvas.after(500, lambda: PlaceStep(i+1))       
    PlaceStep(0)
    
    