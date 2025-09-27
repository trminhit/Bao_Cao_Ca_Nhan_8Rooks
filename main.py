from gui import G_8Quanxe_UI

def main():
    root, canvas, rook_img = G_8Quanxe_UI.WindowUI()
    G_8Quanxe_UI.Draw_start_goal(canvas, rook_img)
    root.mainloop()
    
if __name__ == "__main__":
    main()