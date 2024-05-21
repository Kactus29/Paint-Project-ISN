import tkinter as tk
from tkinter import colorchooser

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint App")
        
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack(expand=True, fill="both")
        
        self.old_x = None
        self.old_y = None
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        
        self.colors = ["black", "red", "green", "blue"]
        self.selected_color = tk.StringVar()
        self.selected_color.set(self.colors[0])
        
        color_frame = tk.Frame(self.root)
        color_frame.pack(side="bottom", fill="x")
        
        for color in self.colors:
            color_btn = tk.Button(color_frame, bg=color, width=3, command=lambda c=color: self.select_color(c))
            color_btn.pack(side="left", padx=2)
        
        custom_color_btn = tk.Button(color_frame, text="Custom Color", command=self.choose_custom_color)
        custom_color_btn.pack(side="left", padx=2)
        
        clear_btn = tk.Button(color_frame, text="Clear", command=self.clear_canvas)
        clear_btn.pack(side="right", padx=2)
        
    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, x1, y1, fill=self.selected_color.get(), width=2)
        self.old_x = x1
        self.old_y = y1
    
    def reset(self, event):
        self.old_x = None
        self.old_y = None
        
    def select_color(self, color):
        self.selected_color.set(color)
        
    def choose_custom_color(self):
        color = colorchooser.askcolor()[1]  # Retourne un tuple (couleur sélectionnée, code hexadécimal)
        if color:
            self.selected_color.set(color)
        
    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
   