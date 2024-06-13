import tkinter as tk
from ZoomableCanvas import ZoomableCanvas
import tkinter.filedialog as fd
import cv2   #pip install opencv-python 

class AsciiArt(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Create an ASCII art")
        self.geometry("300x210")

        self.scale = tk.IntVar()

        self.create_widgets()


    def create_widgets(self):
        self.text = tk.Label(self,text="Veuillez choisir le pourcentage de réduction \n de la taille de l'image")

        self.text.pack()
        
        # Scale widget to select the size of the image by percentage
        self.scale = tk.Scale(self, from_=1, to=100, orient="horizontal", variable=self.scale, label="Pourcentage :")
        self.scale.pack(pady=20)

        self.actualImgB = tk.Button(self, text="Actual Image", command=self.from_image)
        self.actualImgB.pack(pady=5)
        # Open image file
        self.btn_open = tk.Button(self, text="Open Image", command=self.open_image)
        self.btn_open.pack()


    def from_image(self):
        self.load_pixel('asciiart.jpg')

    def open_image(self):
        filetypes = (
            ('Image files', '*.png *.jpg *.jpeg *.gif *.bmp'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        
        if filename:
            self.load_pixel(filename)


#Principe : on calcule l'intensité de chaque pixel. On le compare avec l'intensité de chaque caractère dans la liste pour trouver 
#quel caractère ayant l'intensité le plus proche à celle du pixel. Puis on "remplace" le pixel par le caractère correspondant. 

    def load_pixel(self, file_path):

                

        pixel_ascii_map = " `^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
            #ici, la liste des caractères est déjà arrangée selon l'intensité croissante que représente le caractère 
            #donc on peut supposer que l'ordre de caractère dans la liste est aussi sa l'intensité (dans référence de la liste)
            # Une liste supplémentaire :  pixel_ascii_map = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"


    #fonction imread "lit" le fichier image et revoie les valeurs de pixels sous forme d'une matrice (dont chaque terme dans la matrice est 
    #un tuple de 3 valeurs [R, G, B] qui represente pixel)
        img = cv2.imread(file_path) 

    #on redimensionner la taille d'image selon le voeux d'utilisateur
        img = img[::int(100/self.scale.get()), ::int(100/self.scale.get())]

        ascii_res = ""
        for row in img:
            for pixel in row:
                x = float(sum(pixel)) / 3.0             #on calcule l'intensité moyenne du pixel
                x = (x * len(pixel_ascii_map)) / 255.0  #on convertit la valeur en référence de la liste de caractère (pour comparer à l'intensité du caractère)
                                                        # floor x i.e on choisir la valeur à l'intérieur (par exemple si on a 3.9 on prend la valeur 3)
                x = int(x)                              #comme l'ordre de caractère dans la liste est entier, le x est donc être entier. 
                if x >= len(pixel_ascii_map):
                    x = len(pixel_ascii_map) - 1

                ascii_val = pixel_ascii_map[x]          #on choisit le caractère le plus approprié à l'intensité du pixel
                ascii_res += ascii_val                  #on enregistre le caractère dans un nouveau "text" de caractère

            ascii_res += "\n"                           #si on a exécuté une ligne de pixel de l'image, on passe à la ligne suivant, 
                                                        #ce qui correspond à un saut de ligne dans le nouveau text de caractère 
        #print(img)
        with open("ascii_art_new.txt", "w") as f:
            f.write(ascii_res)                          #on injecte le nouveau text dans un fichier txt pour le regarder.

        if self.scale.get()>50 :
            result=tk.messagebox.askokcancel('Warning','A percentage higher than 50% can be source of lags due to image size. Are you sure you wanna continue with a that high percentage ?' \
                                             ,icon ='warning')
            if result:
                self.show_ascii_art()
        else : 
            self.show_ascii_art()

    def show_ascii_art(self):
        self.destroy()
        AfficherAsciiArt()

class AfficherAsciiArt(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("ASCII Art Rendering")
        # FULLSCREEN
        #self.attributes("-fullscreen", True)
        self.geometry("1200x1200")

        srceen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Bind escape key to exit the program
        self.bind('<Escape>', self.exit_fullscreen)

        #<<<<<Widgets>>>>>>
        #Menu
        menubar = tk.Menu(self)

        options = tk.Menu(menubar, tearoff = 0)
        options.add_command(label="Zoom-in",accelerator="SCROLL UP")
        options.add_command(label="Zoom-out",accelerator="SCROLL DOWN")
        options.add_separator()
        options.add_command(label="Copy into clipboard",command=self.copytxt)
        options.add_command(label="Save as",command=self.savetxtas)
        options.add_separator()
        options.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="Options", menu=options)

        self.config(menu = menubar)

        self.txt=""
        with open("ascii_art_new.txt", "r") as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    self.txt+=str(char)

        #Canva
        canvas = ZoomableCanvas(self, width=srceen_width, height=screen_height)
        canvas.pack()

        with open("ascii_art_new.txt", "r") as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    canvas.create_text(x*10, y*10, text=char)
        
        self.mainloop()

        #==============Menu func===============
    def exit_fullscreen(self,event):
        self.destroy()

    def copytxt(self):
        self.clipboard_clear()
        self.clipboard_append(self.txt)

    def savetxtas(self):
        file_path=fd.asksaveasfilename(initialdir = "/",title = "Select folder",filetypes = (("txt files",".txt"),("all files",".*"))) + ".txt"
        with open(file_path, "w") as f:
            f.write(self.txt)
