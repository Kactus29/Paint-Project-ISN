import tkinter as tk
from ZoomableCanvas import ZoomableCanvas

class AfficherAsciiArt(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("ASCII Art")
        # FULLSCREEN
        self.attributes("-fullscreen", True)

        srceen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        canvas = ZoomableCanvas(self, width=srceen_width, height=screen_height)
        canvas.pack()

        with open("ascii_art_new.txt", "r") as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    canvas.create_text(x*10, y*10, text=char)

        # Bind escape key to exit the program
        self.bind("<Escape>", lambda e: self.quit())

        self.mainloop()

    def quit(self):
        self.destroy()
