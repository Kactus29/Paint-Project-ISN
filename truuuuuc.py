import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk
import utility
import modify_picture

class Paint(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Le Paint du pauvre")
        self.resizable(True, True)
        self.minsize(530, 400)
        self.geometry("730x560")

        self.width = 730
        self.height = 560

        self.initvar()
        self.initwidget()

    def initvar(self):
        self.quillsize = tk.DoubleVar()
        self.color = (0, 0, 0)

        self.cursor = {}
        self.cursorCount = 0

        self.actualtool = "quill"
        self.icons = {}
        self.custom_cursors = {
            'quill': 'pencil',
            'fill': 'spraycan',
            'resize': 'sizing',
            'handle': 'hand2'
        }

        self.picture = {'height': 420, 'width': 420, 'img': Image.new('RGB', (420, 420), (255, 255, 255))}

        self.old_draw = [self.picture['img'].copy()]
        self.new_draw = []

    def initwidget(self):
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
        editMenu.add_command(label="Undo", accelerator="CTRL+Z", command=self.undo_command)
        editMenu.add_command(label="Redo", accelerator="CTRL+Y", command=self.redo_command)
        editMenu.add_command(label="Clear", command=self.clearcanva)
        editMenu.add_separator()
        editMenu.add_command(label="Convert ASCII into art", command=self.convertASCII)
        menubar.add_cascade(label="Edit", menu=editMenu)

        self.config(menu=menubar)

        self.icons['quill'] = utility.load_icon('quill_icon.png')
        self.quillB = tk.Button(self, bg="lightgrey", width=25, height=25, image=self.icons['quill'])
        self.quillB.bind('<Button-1>', self.quilltool)
        self.quillB.place(x=10, y=20)

        self.icons['paint_can'] = utility.load_icon('paint_can_icon.png')
        self.fillB = tk.Button(self, bg="lightgrey", width=25, height=25, image=self.icons['paint_can'])
        self.fillB.bind('<Button-1>', self.filltool)
        self.fillB.place(x=60, y=20)

        self.sizeL = tk.Label(self, text="Quill Size :")
        self.sizeL.place(x=120, y=25)

        self.scaleQuill = tk.Scale(self, orient='horizontal', from_=0, to=100, resolution=1, tickinterval=25, length=200, variable=self.quillsize)
        self.scaleQuill.place(x=185, y=5)

        self.colorL = tk.Label(self, text='#000000', font=("Arial", 10))
        self.colorL.place(x=480, y=25)

        self.icons['color_palette'] = utility.load_icon('color_palette_icon.png')
        self.colorB = tk.Button(self, bg="lightgrey", width=25, height=25, image=self.icons['color_palette'])
        self.colorB.bind('<Button-1>', self.selectcolor)
        self.colorB.place(x=440, y=20)

        self.canva = tk.Canvas(self, bg="white", width=self.picture['width'], height=self.picture['height'])

        self.canva.create_image(self.picture['width'], self.picture['height'], image=ImageTk.PhotoImage(self.picture['img']))
        self.canva.image = ImageTk.PhotoImage(self.picture['img'])

        self.canva.bind('<Motion>', self.cursormove)
        self.canva.bind('<Leave>', self.cursorquit)
        self.canva.bind('<Button-1>', self.onLeftClick)
        self.canva.bind('<B1-Motion>', self.onLeftClick)
        self.canva.bind('<ButtonRelease-1>', self.add_undo_log_command)
        self.canva.bind('<B3-Motion>', self.onRightClick)
        self.canva.bind('<Button-3>', self.onRightClick)
        self.canva.bind('<ButtonRelease-3>', self.add_undo_log_command)

        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)

        self.bind('<Configure>', self.resize)

        self.canva.place(x=290, y=120)

        self.canva.config(cursor=self.custom_cursors['quill'])

        self.handle_size = 10
        self.handle = self.canva.create_rectangle(self.picture['width'] - self.handle_size, self.picture['height'] - self.handle_size,
                                                  self.picture['width'], self.picture['height'], fill='blue', tags='handle')
        self.canva.tag_bind('handle', '<ButtonPress-1>', self.on_handle_press)
        self.canva.tag_bind('handle', '<B1-Motion>', self.on_handle_drag)
        self.canva.tag_bind('handle', '<Enter>', self.on_handle_enter)
        self.canva.tag_bind('handle', '<Leave>', self.on_handle_leave)

    def on_handle_press(self, event):
        self.handle_press_x = event.x
        self.handle_press_y = event.y

    def on_handle_drag(self, event):
        dx = event.x - self.handle_press_x
        dy = event.y - self.handle_press_y

        new_width = self.picture['width'] + dx
        new_height = self.picture['height'] + dy

        if new_width > self.handle_size and new_height > self.handle_size:
            self.canva.config(width=new_width, height=new_height)
            self.picture['width'] = new_width
            self.picture['height'] = new_height

            self.canva.coords(self.handle, new_width - self.handle_size, new_height - self.handle_size,
                              new_width, new_height)

            self.picture['img'] = self.picture['img'].resize((new_width, new_height))
            self.refresh()

            self.handle_press_x = event.x
            self.handle_press_y = event.y

    def on_handle_enter(self, event):
        self.canva.config(cursor=self.custom_cursors['handle'])

    def on_handle_leave(self, event):
        self.canva.config(cursor=self.custom_cursors[self.actualtool])

    def resize(self, event):
        if event.widget == self:
            width = self.winfo_width() - 310
            height = self.winfo_height() - 140

            self.width = width
            self.height = height

    def newpic(self):
        newpic = Newpic(self)
        newpic.grab_set()

    def loadpic(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpg files", ".jpg"), ("png files", ".png"), ("all files", ".")))
        self.picture['img'] = Image.open(self.filename)

        self.picture['width'], self.picture['height'] = self.picture['img'].size
        self.canva["width"] = self.picture['width']
        self.canva["height"] = self.picture['height']

        self.filename = self.filename[:-4]

        self.refresh()

    def savepicas(self):
        self.filename = filedialog.asksaveasfilename(initialdir="/", title="Select folder", filetypes=(("jpg files", ".jpg"), ("all files", ".*")))
        self.picture['img'].save(self.filename + ".jpg")

    def savepic(self):
        try:
            self.picture['img'].save(self.filename + ".jpg")
        except:
            self.filename = filedialog.asksaveasfilename(initialdir="/", title="Select folder", filetypes=(("jpg files", ".jpg"), ("all files", ".*")))
            self.picture['img'].save(self.filename + ".jpg")

    def clearcanva(self):
        self.picture['img'] = Image.new('RGB', (self.picture['width'], self.picture['height']), (255, 255, 255))

        self.add_undo_log()

        self.refresh()

        self.new_draw = []

    def convertASCII(self):
        self.picture['img'].save('asciiart.jpg')
        AsciiArt()

    def selectcolor(self, event):
        color = colorchooser.askcolor()[1]
        if color:
            self.color = utility.HexToDec(color)
            self.colorL["text"] = color

    def refresh(self):
        img_tk = ImageTk.PhotoImage(self.picture['img'])
        x = int(self.picture['width'] / 2)
        y = int(self.picture['height'] / 2)

        self.canva.delete("all")
        self.canva.create_image(x, y, image=img_tk)
        self.canva.image = img_tk

        self.handle = self.canva.create_rectangle(self.picture['width'] - self.handle_size, self.picture['height'] - self.handle_size,
                                                  self.picture['width'], self.picture['height'], fill='blue', tags='handle')
        self.canva.tag_bind('handle', '<ButtonPress-1>', self.on_handle_press)
        self.canva.tag_bind('handle', '<B1-Motion>', self.on_handle_drag)
        self.canva.tag_bind('handle', '<Enter>', self.on_handle_enter)
        self.canva.tag_bind('handle', '<Leave>', self.on_handle_leave)

    def cursormove(self, event):
        cursize = int(self.quillsize.get() / 2)
        self.cursor[f"id{self.cursorCount}"] = self.canva.create_oval(event.x - cursize, event.y - cursize, event.x + cursize, event.y + cursize, outline="black")
        try:
            self.canva.delete(self.cursor[f"id{self.cursorCount - 1}"])
        except KeyError:
            pass
        self.cursorCount += 1

    def cursorquit(self, event):
        try:
            self.canva.delete(self.cursor[f"id{self.cursorCount - 1}"])
            self.cursorCount = 0
        except KeyError:
            pass

    def quilltool(self, event):
        if self.actualtool != "quill":
            self.actualtool = "quill"
            self.canva.config(cursor=self.custom_cursors['quill'])

    def filltool(self, event):
        if self.actualtool != "fill":
            self.actualtool = "fill"
            self.canva.config(cursor=self.custom_cursors['fill'])

    def onLeftClick(self, event):
        if len(self.new_draw) > 0:
            self.new_draw = []

        if self.actualtool == "quill":
            cursize = int(self.quillsize.get() / 2)
            self.picture['img'] = modify_picture.modify_trace(self.picture['img'], self.color, event.x, event.y, cursize, self.picture['width'], self.picture['height'])
            self.refresh()

        if self.actualtool == "fill":
            self.picture['img'] = modify_picture.modify_fill(self.picture['img'], event.x, event.y, self.color)
            self.refresh()

    def onRightClick(self, event):
        if self.actualtool == "quill":
            cursize = int(self.quillsize.get() / 2)
            self.picture['img'] = modify_picture.modify_trace(self.picture['img'], (255, 255, 255), event.x, event.y, cursize, self.picture['width'], self.picture['height'])
            self.refresh()
            self.cursor[f"id{self.cursorCount}"] = self.canva.create_oval(event.x - cursize, event.y - cursize, event.x + cursize, event.y + cursize, outline="black")
            try:
                self.canva.delete(self.cursor[f"id{self.cursorCount - 1}"])
            except KeyError:
                pass
            self.cursorCount += 1

    def add_undo_log_command(self, command):
        self.add_undo_log()

    def add_undo_log(self):
        self.old_draw.append(self.picture['img'].copy())

    def undo(self, event):
        self.undo_command()

    def undo_command(self):
        if len(self.old_draw) > 1:
            self.new_draw.append(self.old_draw.pop(-1))
            self.picture['img'] = self.old_draw[-1]
            self.refresh()

    def redo(self, event):
        self.redo_command()

    def redo_command(self):
        if len(self.new_draw) > 0:
            self.picture['img'] = self.new_draw.pop(-1)
            self.old_draw.append(self.picture['img'].copy())
            self.refresh()

class Newpic(tk.Toplevel):
    def __init__(self, parent):
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
        self.parent.picture['width'] = int(self.EntWidth.get())
        self.parent.picture['height'] = int(self.EntHeight.get())
        self.parent.canva["width"] = self.parent.picture['width']
        self.parent.canva["height"] = self.parent.picture['height']
        self.parent.picture['img'] = Image.new('RGB', (self.parent.picture['width'], self.parent.picture['height']), (255, 255, 255))
        self.parent.canva.delete("all")
        self.parent.canva.config(scrollregion=(0, 0, self.parent.picture['width'], self.parent.picture['height']))
        self.destroy()

app = Paint()
app.mainloop()
