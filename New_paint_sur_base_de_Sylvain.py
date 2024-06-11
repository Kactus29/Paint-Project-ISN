import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw
import render_color
import modify_picture
import ascii_art
import remplissage

class Paint(tk.Tk):
    """
    Main Paint application class.
    """
    def __init__(self):
        """
        Initialize the main Paint application window.
        """
        super().__init__()
        self.title("Le Paint du pauvre")
        self.resizable(True, True)
        self.minsize(530, 400)
        self.geometry("730x560")
        
        self.initvar()
        self.initwidget()
    
    def initvar(self):
        """
        Initialize the application variables.
        """
        self.pensize = tk.DoubleVar()
        self.color = (0, 0, 0)
        self.cursor = {}
        self.cursorCount = 0
        self.actualtool = "pen"
        
        self.picture = {
            'height': 420, 
            'width': 420, 
            'img': Image.new('RGB', (420, 420), (255, 255, 255)),
            'draw': ImageDraw.Draw(Image.new('RGB', (420, 420), (255, 255, 255)))
        }

    def initwidget(self):
        """
        Initialize the application widgets.
        """
        menubar = tk.Menu(self)

        options = tk.Menu(menubar, tearoff=0)
        options.add_command(label="New", command=self.newpic)
        options.add_command(label="Load", command=self.loadpic)
        options.add_command(label="Save as", command=self.savepicas)
        options.add_command(label="Save", command=self.savepic)
        options.add_separator()
        options.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=options)

        editMenu = tk.Menu(menubar, tearoff=0)
        editMenu.add_command(label="Undo")
        editMenu.add_command(label="Redo")
        editMenu.add_command(label="Clear", command=self.clearcanva)
        editMenu.add_separator()
        editMenu.add_command(label="Convert ASCII into art", command=self.convertASCII)
        menubar.add_cascade(label="Edit", menu=editMenu)
        
        self.config(menu=menubar)
        
        self.fillB = tk.Button(self, text="P", bg="lightgreen", fg='black', width=3, height=1)
        self.fillB.bind('<Button-1>', self.pentool)
        self.fillB.place(x=10, y=20)
        
        self.sizeL = tk.Label(self, text="Pen Size :")
        self.sizeL.place(x=110, y=25)
        
        self.scalePen = tk.Scale(self, orient='horizontal', from_=0, to=100, resolution=1, tickinterval=25, length=200, variable=self.pensize)
        self.scalePen.place(x=200, y=5)
        
        self.fillB = tk.Button(self, text="F", bg="lightgrey", fg='black', width=3, height=1)
        self.fillB.bind('<Button-1>', self.filltool)
        self.fillB.place(x=60, y=20)

        self.colorL = tk.Label(self, text='#000000')
        self.colorL.place(x=20, y=90)
        
        self.colorB = tk.Button(self, text="C", bg="lightgrey", fg='black', width=3, height=1)
        self.colorB.bind('<Button-1>', self.selectcolor)
        self.colorB.place(x=450, y=20)

        self.canva = tk.Canvas(self, bg="white", width=self.picture['width'], height=self.picture['height'])
        self.canva.place(x=290, y=120)
        self.refresh()

        self.canva.bind('<Motion>', self.cursormove)
        self.canva.bind('<Leave>', self.cursorquit)
        self.canva.bind('<B1-Motion>', self.trace)
        self.canva.bind('<Button-1>', self.start_trace)
        
        self.canva.bind('<B3-Motion>', self.erase)
        self.canva.bind('<Button-3>', self.erase)
        
        self.bind('<Configure>', self.resize)
    
    def resize(self, event):
        """
        Handle window resize events.
        """
        if event.widget == self:
            width = self.winfo_width() - 310
            height = self.winfo_height() - 140
            self.canva.config(width=width, height=height)
            self.refresh()
    
    def newpic(self):
        """
        Create a new picture.
        """
        newpic = Newpic(self)
        newpic.grab_set()

    def loadpic(self):
        """
        Load a picture from a file.
        """
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))
        if self.filename:
            self.picture['img'] = Image.open(self.filename)
            self.picture['draw'] = ImageDraw.Draw(self.picture['img'])
            self.picture['width'], self.picture['height'] = self.picture['img'].size
            self.canva.config(width=self.picture['width'], height=self.picture['height'])
            self.filename = self.filename[:-4]
            self.refresh()

    def savepicas(self):
        """
        Save the current picture as a new file.
        """
        self.filename = filedialog.asksaveasfilename(initialdir="/", title="Select folder", filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
        if self.filename:
            self.picture['img'].save(self.filename + ".jpg")

    def savepic(self):
        """
        Save the current picture.
        """
        try:
            self.picture['img'].save(self.filename + ".jpg")
        except AttributeError:
            self.savepicas()
    
    def clearcanva(self):
        """
        Clear the canvas.
        """
        self.canva.delete("all")
        self.picture['img'] = Image.new('RGB', (self.picture['width'], self.picture['height']), (255, 255, 255))
        self.picture['draw'] = ImageDraw.Draw(self.picture['img'])
        self.refresh()

    def convertASCII(self):
        """
        Convert the current picture to ASCII art.
        """
        ascii_window = tk.Toplevel(self)
        ascii_window.title("ASCII Art")
        
        ascii_art_str = ascii_art.convert_image_to_ascii(self.picture['img'])
        ascii_text = tk.Text(ascii_window)
        ascii_text.insert(tk.END, ascii_art_str)
        ascii_text.pack(expand=True, fill='both')

    def selectcolor(self, event):
        """
        Open a color chooser dialog to select a color.
        """
        color = colorchooser.askcolor()[1]
        if color:
            self.color = render_color.HexToDec(color)
            self.colorL["text"] = color

    def refresh(self):
        """
        Refresh the canvas with the current picture.
        """
        self.canva.delete("all")
        img_tk = ImageTk.PhotoImage(self.picture['img'])
        self.canva.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canva.image = img_tk

    def cursormove(self, event):
        """
        Handle cursor movement events on the canvas.
        """
        if self.actualtool == "pen":
            cursize = int(self.pensize.get() / 2)
            self.cursor[f"id{self.cursorCount}"] = self.canva.create_oval(event.x - cursize, event.y - cursize, event.x + cursize, event.y + cursize, outline="black")
            try:
                self.canva.delete(self.cursor[f"id{self.cursorCount - 1}"])
            except KeyError:
                pass
            self.cursorCount += 1

    def cursorquit(self, event):
        """
        Handle cursor leave events on the canvas.
        """
        try:
            self.canva.delete(self.cursor[f"id{self.cursorCount - 1}"])
        except KeyError:
            pass
        self.cursorCount = 0

    def pentool(self, event):
        """
        Set the current tool to pen.
        """
        if self.actualtool != "pen":
            self.actualtool = "pen"

    def start_trace(self, event):
        """
        Start tracing a line.
        """
        self.old_x, self.old_y = event.x, event.y

    def trace(self, event):
        """
        Trace a line on the canvas.
        """
        if self.actualtool == "pen":
            cursize = int(self.pensize.get())
            self.picture['draw'].line([(self.old_x, self.old_y), (event.x, event.y)], fill=self.color, width=cursize)
            self.old_x, self.old_y = event.x, event.y
            self.refresh()

    def erase(self, event):
        """
        Erase a portion of the drawing on the canvas.
        """
        cursize = int(self.pensize.get())
        self.picture['draw'].line([(self.old_x, self.old_y), (event.x, event.y)], fill=(255, 255, 255), width=cursize)
        self.old_x, self.old_y = event.x, event.y
        self.refresh()

    def filltool(self, event):
        """
        Set the current tool to fill.
        """
        if self.actualtool != "fill":
            self.actualtool = "fill"
            self.canva.bind('<Button-1>', self.fill)

    def fill(self, event):
        """
        Fill a region with the selected color.
        """
        remplissage.modify_fill(self.picture['img'], event.x, event.y, self.color)
        self.refresh()

class Newpic(tk.Toplevel):
    """
    Toplevel window for creating a new picture.
    """
    def __init__(self, parent):
        """
        Initialize the Newpic window.
        """
        tk.Toplevel.__init__(self, parent)
        self.parent = parent

        self.geometry('500x200')
        self.title('New picture')
        self.resizable(False, False)
        
        self.WidthL = tk.Label(self, text="Width :")
        self.EntWidth = tk.Entry(self)
        self.pxL1 = tk.Label(self, text="px")
        self.WidthL.place(x=10, y=25)
        self.EntWidth.place(x=80, y=25, width=50)
        self.pxL1.place(x=135, y=25)
        self.EntWidth.focus()
    
        self.HeightL = tk.Label(self, text="Height :")
        self.EntHeight = tk.Entry(self)
        self.pxL2 = tk.Label(self, text="px")
        self.HeightL.place(x=170, y=25)
        self.EntHeight.place(x=240, y=25, width=50)
        self.pxL2.place(x=295, y=25)
        
        self.CancelB = tk.Button(self, text='Cancel', command=self.destroy)
        self.CancelB.place(x=180, y=120)
        self.CreateB = tk.Button(self, text='Create')
        self.CreateB.bind('<Button-1>', self.createCanva)
        self.CreateB.place(x=280, y=120)

    def createCanva(self, event):
        """
        Create a new canvas with the specified width and height.
        """
        self.parent.picture['width'] = int(self.EntWidth.get())
        self.parent.picture['height'] = int(self.EntHeight.get())
        self.parent.canva.config(width=self.parent.picture['width'], height=self.parent.picture['height'])
        self.parent.picture['img'] = Image.new('RGB', (self.parent.picture['width'], self.parent.picture['height']), (255, 255, 255))
        self.parent.picture['draw'] = ImageDraw.Draw(self.parent.picture['img'])
        self.parent.canva.delete("all")
        self.parent.refresh()
        self.destroy()

# Create the main application instance and run it
app = Paint()
app.mainloop()
