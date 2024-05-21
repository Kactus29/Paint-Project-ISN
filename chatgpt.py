import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        # Ajouter un bouton pour ouvrir une image
        self.open_button = tk.Button(root, text="Open Image", command=self.open_image)
        self.open_button.pack(side=tk.LEFT)
        
        # Ajouter un bouton pour sauvegarder l'image
        self.save_button = tk.Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack(side=tk.LEFT)
        
        # Ajouter un bouton pour annuler la dernière action
        self.undo_button = tk.Button(root, text="Undo", command=self.undo_last_action)
        self.undo_button.pack(side=tk.LEFT)

        # Variable pour stocker l'image affichée
        self.image_on_canvas = None
        self.image = None
        self.draw = None
        self.actions = []  # Pour stocker les actions pour l'annulation

        # Configurer les événements de dessin
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        
        # Configurer l'événement pour CTRL+Z
        root.bind("<Control-z>", self.undo_last_action)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if file_path:
            self.display_image(file_path)

    def display_image(self, file_path):
        # Charger l'image
        self.image = Image.open(file_path).convert("RGB")
        
        # Redimensionner l'image pour qu'elle s'adapte au canvas
        self.image = self.image.resize((800, 600), Image.ANTIALIAS)
        
        # Convertir l'image en PhotoImage
        self.photo = ImageTk.PhotoImage(self.image)
        
        # Afficher l'image sur le canvas
        if self.image_on_canvas is None:
            self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        else:
            self.canvas.itemconfig(self.image_on_canvas, image=self.photo)

        # Configurer ImageDraw pour dessiner sur l'image
        self.draw = ImageDraw.Draw(self.image)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg")])
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Save Image", "Image saved successfully.")

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=5)
        self.actions.append((x1, y1, x2, y2))
        
        if self.draw:
            self.draw.line([x1, y1, x2, y2], fill="black", width=5)

    def reset(self, event):
        pass

    def undo_last_action(self, event=None):
        if self.actions:
            self.actions.pop()
            self.redraw_image()

    def redraw_image(self):
        # Redessiner l'image de base
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Rejouer toutes les actions sauvegardées
        for action in self.actions:
            x1, y1, x2, y2 = action
            self.draw.line([x1, y1, x2, y2], fill="black", width=5)

        # Mettre à jour l'affichage sur le canvas
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.photo)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
