import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog
from PIL import Image, ImageTk, ImageGrab
from remplissage import flood_fill, colorie_pixels

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
        
        size_btn = tk.Button(self.color_frame, text="Size", command=self.change_size)
        size_btn.pack(side="left", padx=2)

        fill_btn = tk.Button(self.color_frame, text="Fill", command=self.perform_fill)
        fill_btn.pack(side="left", padx=2)

        open_btn = tk.Button(self.color_frame, text="Open", command=self.open_image)
        open_btn.pack(side="right", padx=2)
        
        save_btn = tk.Button(self.color_frame, text="Save", command=self.save_image)
        save_btn.pack(side="right", padx=2)
        
        pencil_btn = tk.Button(self.color_frame, text="Pencil", command=self.pencil_tool)
        pencil_btn.pack(side="right", padx=2)
        
        # Création du canevas
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack(expand=True, fill="both")
        
        # Initialisation des variables
        self.selected_color = "black"  # Initialiser avec la couleur noire par défaut
        self.selected_size = 2  # Taille du pinceau par défaut
        self.pencil_tool()

        # Gestion des événements du canevas
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
    
    def pencil_tool(self):
        self.canvas.config(cursor="pencil")
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def start_drawing(self, event):
        self.old_x, self.old_y = event.x, event.y
    
    def draw(self, event):
        x, y = event.x, event.y
        self.canvas.create_line(self.old_x, self.old_y, x, y, fill=self.selected_color, width=self.selected_size)
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

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            x0 = self.canvas.winfo_rootx() + self.canvas.winfo_x()
            y0 = self.canvas.winfo_rooty() + self.canvas.winfo_y()
            x1 = x0 + self.canvas.winfo_width()
            y1 = y0 + self.canvas.winfo_height()
            
            img = ImageGrab.grab((x0, y0, x1, y1))
            img.save(file_path)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            img = Image.open(file_path)
            self.tk_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
    
    def change_size(self):
        size_window = tk.Toplevel(self.root)
        size_window.title("Change Size")
        
        size_scale = tk.Scale(size_window, from_=1, to=20, orient="horizontal", label="Size", command=self.update_size)
        size_scale.set(self.selected_size)
        size_scale.pack(padx=10, pady=10)
    
    def update_size(self, value):
        self.selected_size = int(value)

    def perform_fill(self):
        # Obtenir les coordonnées du clic de l'utilisateur
        x, y = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(), self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        
        # Obtenir l'image du canevas
        x0 = self.canvas.winfo_rootx() + self.canvas.winfo_x()
        y0 = self.canvas.winfo_rooty() + self.canvas.winfo_y()
        x1 = x0 + self.canvas.winfo_width()
        y1 = y0 + self.canvas.winfo_height()
        img = ImageGrab.grab((x0, y0, x1, y1))

        # Appliquer le remplissage
        flood_filled_img = flood_fill(img, x, y)

        # Mettre à jour le canevas avec l'image remplie
        self.tk_image = ImageTk.PhotoImage(flood_filled_img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()

