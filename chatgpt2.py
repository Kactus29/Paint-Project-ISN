import tkinter as tk
from tkinter import colorchooser, messagebox

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint App")
        
        # Création des boutons
        self.color_frame = tk.Frame(self.root)
        self.color_frame.pack(side="top", fill="x")
        
        self.colors = ["black", "red", "orange", "yellow", "green", "light blue", "dark blue"]
        
        for color in self.colors:
            color_btn = tk.Button(self.color_frame, bg=color, width=5, command=lambda c=color: self.select_color(c))
            color_btn.pack(side="left", padx=2)
        
        custom_color_btn = tk.Button(self.color_frame, text="Custom Color", command=self.choose_custom_color)
        custom_color_btn.pack(side="left", padx=2)
        
        clear_btn = tk.Button(self.color_frame, text="Clear All", command=self.clear_all)
        clear_btn.pack(side="right", padx=2)
        
        # Création du canevas
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack(expand=True, fill="both")
        
        # Initialisation des variables
        self.selected_color = "black"  # Initialiser avec la couleur noire par défaut
        
        # Gestion des événements du canevas
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        
    def start_drawing(self, event):
        self.old_x, self.old_y = event.x, event.y
    
    def draw(self, event):
        x, y = event.x, event.y
        self.canvas.create_line(self.old_x, self.old_y, x, y, fill=self.selected_color, width=2)
        self.old_x, self.old_y = x, y
    
    def stop_drawing(self, event):
        pass
        
    def select_color(self, color):
        self.selected_color = color
        
    def choose_custom_color(self):
        color = colorchooser.askcolor()[1]  # Retourne un tuple (couleur sélectionnée, code hexadécimal)
        if color:
            self.selected_color = color
            
    def clear_all(self):
        confirmation = messagebox.askyesno("Clear All", "Are you sure you want to clear all drawings?")
        if confirmation:
            self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
