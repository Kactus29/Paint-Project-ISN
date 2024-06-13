import tkinter as tk
from ZoomableCanvas import ZoomableCanvas
import tkinter.filedialog as fd
import cv2   #pip install opencv-python 

class AsciiArt(tk.Tk):
    """
    Classe principale pour créer une interface graphique permettant de générer de l'art ASCII à partir d'images.

    Hérite de la classe Tk de tkinter pour créer une fenêtre principale avec des widgets.

    Méthodes
    ----------
    __init__():
        Initialise la fenêtre principale et les variables nécessaires.
    
    create_widgets():
        Crée et place les widgets dans la fenêtre principale.
    
    from_image():
        Charge une image par défaut 'asciiart.jpg' et la transforme en art ASCII.
    
    open_image():
        Ouvre une boîte de dialogue pour sélectionner une image à convertir en art ASCII.
    
    load_pixel(file_path: str):
        Charge l'image, redimensionne, calcule l'art ASCII et enregistre le résultat dans un fichier texte.
    
    show_ascii_art():
        Affiche l'art ASCII généré dans une nouvelle fenêtre.
    """
    def __init__(self):
        super().__init__()
        self.title("Créer un art ASCII")
        self.geometry("300x210")
        self.scale = tk.IntVar()
        self.create_widgets()

    def create_widgets(self):
        self.text = tk.Label(self, text="Veuillez choisir le pourcentage de réduction \n de la taille de l'image")
        self.text.pack()
        
        # Widget de scale pour sélectionner la taille de l'image en pourcentage
        self.scale = tk.Scale(self, from_=1, to=100, orient="horizontal", variable=self.scale, label="Pourcentage :")
        self.scale.pack(pady=20)

        self.actualImgB = tk.Button(self, text="Image Actuelle", command=self.from_image)
        self.actualImgB.pack(pady=5)
        
        # Bouton pour ouvrir un fichier image
        self.btn_open = tk.Button(self, text="Ouvrir Image", command=self.open_image)
        self.btn_open.pack()

    def from_image(self):
        self.load_pixel('asciiart.jpg')

    def open_image(self):
        filetypes = (
            ('Fichiers image', '*.png *.jpg *.jpeg *.gif *.bmp'),
            ('Tous les fichiers', '*.*')
        )

        filename = fd.askopenfilename(
            title='Ouvrir un fichier',
            initialdir='/',
            filetypes=filetypes)
        
        if filename:
            self.load_pixel(filename)

    def load_pixel(self, file_path):
        """
        Charge l'image à partir du chemin fourni, la redimensionne selon le pourcentage choisi,
        convertit les pixels en caractères ASCII, et enregistre le résultat dans un fichier texte.

        Paramètres
        ----------
        file_path : str
            Chemin de l'image à charger.
        """
        pixel_ascii_map = " `^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
        
        img = cv2.imread(file_path)
        img = img[::int(100/self.scale.get()), ::int(100/self.scale.get())]

        ascii_res = ""
        for row in img:
            for pixel in row:
                x = float(sum(pixel)) / 3.0
                x = (x * len(pixel_ascii_map)) / 255.0
                x = int(x)
                if x >= len(pixel_ascii_map):
                    x = len(pixel_ascii_map) - 1

                ascii_val = pixel_ascii_map[x]
                ascii_res += ascii_val

            ascii_res += "\n"

        with open("ascii_art_new.txt", "w") as f:
            f.write(ascii_res)

        if self.scale.get() > 50:
            result = tk.messagebox.askokcancel(
                'Warning',
                'Un pourcentage supérieur à 50% peut causer des ralentissements en raison de la taille de l\'image. '
                'Êtes-vous sûr de vouloir continuer avec un pourcentage aussi élevé ?',
                icon='warning'
            )
            if result:
                self.show_ascii_art()
        else:
            self.show_ascii_art()

    def show_ascii_art(self):
        self.destroy()
        AfficherAsciiArt()

class AfficherAsciiArt(tk.Tk):
    """
    Classe pour afficher l'art ASCII généré dans une nouvelle fenêtre.

    Hérite de la classe Tk de tkinter pour créer une fenêtre avec des options de menu et un canvas zoomable.

    Méthodes
    ----------
    __init__():
        Initialise la fenêtre d'affichage de l'art ASCII avec un menu et un canvas.
    
    exit_fullscreen(event):
        Permet de quitter le mode plein écran.
    
    copytxt():
        Copie l'art ASCII dans le presse-papiers.
    
    savetxtas():
        Sauvegarde l'art ASCII dans un fichier texte.
    """
    def __init__(self):
        super().__init__()
        self.title("Affichage de l'art ASCII")
        self.geometry("1200x1200")

        srceen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Bind escape key to exit the program
        self.bind('<Escape>', self.exit_fullscreen)

        # Menu
        menubar = tk.Menu(self)

        options = tk.Menu(menubar, tearoff=0)
        options.add_command(label="Zoom avant", accelerator="SCROLL UP")
        options.add_command(label="Zoom arrière", accelerator="SCROLL DOWN")
        options.add_separator()
        options.add_command(label="Copier dans le presse-papiers", command=self.copytxt)
        options.add_command(label="Sauvegarder sous", command=self.savetxtas)
        options.add_separator()
        options.add_command(label="Quitter", command=self.destroy)
        menubar.add_cascade(label="Options", menu=options)

        self.config(menu=menubar)

        self.txt = ""
        with open("ascii_art_new.txt", "r") as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    self.txt += str(char)

        # Canvas
        canvas = ZoomableCanvas(self, width=srceen_width, height=screen_height)
        canvas.pack()

        with open("ascii_art_new.txt", "r") as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    canvas.create_text(x * 10, y * 10, text=char)
        
        self.mainloop()

    def exit_fullscreen(self, event):
        self.destroy()

    def copytxt(self):
        self.clipboard_clear()
        self.clipboard_append(self.txt)

    def savetxtas(self):
        file_path = fd.asksaveasfilename(
            initialdir="/",
            title="Sélectionner le dossier",
            filetypes=(("fichiers txt", ".txt"), ("tous les fichiers", ".*"))
        ) + ".txt"
        with open(file_path, "w") as f:
            f.write(self.txt)
