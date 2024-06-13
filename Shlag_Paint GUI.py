import tkinter as tk
from tkinter import filedialog, colorchooser
import numpy as np
from PIL import Image, ImageTk
import cv2 #pip install opencv-python 
import shutil

import render_color
import utility
import modify_picture
import remplissage
from ascii_art import AsciiArt

class Paint(tk.Tk):
    
    #======================Init (main loop)=========================#
    
    def __init__(self):
        super().__init__()
        self.title("Le Paint du pauvre")
        self.resizable(True,True)
        self.minsize(530,400)
        self.geometry("730x560")
        
        self.width=730
        self.height=560

        self.old_draw = []
        self.new_draw = []
        
        self.initvar()
        self.initwidget()
    
    #======================Sub func Init========================#
    
    #var#
    def initvar(self):
        self.quillsize=tk.DoubleVar()
        self.color=(0,0,0)

        self.cursor={}
        self.cursorCount = 0

        self.actualtool="quill"
        self.icons={}
        self.custom_cursors = {
            'quill' : 'pencil',
            'fill' : 'spraycan'
            }
        
        self.picture={'height':420,'width':420,'img': Image.new('RGB',(420, 420),(255,255,255))}
        

    #widget#
    def initwidget(self):
        #Menu
        menubar = tk.Menu(self)

        options = tk.Menu(menubar, tearoff = 0)
        options.add_command(label="New",command=self.newpic)
        options.add_command(label="Load",command=self.loadpic)
        options.add_command(label="Save as",command=self.savepicas)
        options.add_command(label="Save",command=self.savepic)
        options.add_separator()
        options.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=options)

        editMenu = tk.Menu(menubar, tearoff = 0)
        editMenu.add_command(label="Undo",accelerator="CTRL+Z", command=self.undo_command)
        editMenu.add_command(label="Redo",accelerator="CTRL+Y", command=self.redo_command)
        editMenu.add_command(label="Clear", command=self.clearcanva)
        editMenu.add_separator()
        editMenu.add_command(label="Convert ASCII into art", command=self.convertASCII)
        menubar.add_cascade(label="Edit", menu=editMenu)
        
        self.config(menu = menubar)
        
        #quill tool
        self.icons['quill'] = utility.load_icon('quill_icon.png')
        self.quillB=tk.Button(self,bg="lightgrey", width=25, height=25, image=self.icons['quill'])
        self.quillB.bind('<Button-1>',self.quilltool)
        self.quillB.place(x=10,y=20)
        
        #fill tool
        self.icons['paint_can'] = utility.load_icon('paint_can_icon.png')
        self.fillB=tk.Button(self,bg="lightgrey", width=25, height=25, image=self.icons['paint_can'])
        self.fillB.bind('<Button-1>',self.filltool)
        self.fillB.place(x=60,y=20)

        #size scale quill
        self.sizeL = tk.Label(self,text="Quill Size :")
        self.sizeL.place(x=120,y=25)
        
        self.scaleQuill = tk.Scale(self, orient='horizontal', from_= 0, to = 100,resolution=1, tickinterval=25, length=200,variable = self.quillsize)
        self.scaleQuill.place(x=185,y=5)

        #color canva
        self.colorL = tk.Label(self,text='#000000',font=("Arial", 10))
        self.colorL.place(x=480,y=25)
        
        self.icons['color_palette'] = utility.load_icon('color_palette_icon.png')
        self.colorB = tk.Button(self, bg="lightgrey", width=25, height=25, image=self.icons['color_palette'])
        self.colorB.bind('<Button-1>',self.selectcolor)
        self.colorB.place(x=440,y=20)

        #main canva
        self.canva=tk.Canvas(self,bg="white",width=self.picture['width'],height=self.picture['height'])
        
        self.canva.create_image(self.picture['width'],self.picture['height'],image=ImageTk.PhotoImage(self.picture['img'])) #<----------------------------last edit
        self.canva.image=ImageTk.PhotoImage(self.picture['img']) #<----------------------------last edit
        
        self.canva.bind('<Motion>',self.cursormove) #The mouse is moved, with mouse button 1 being held down (use B2 for the middle button, B3 for the right button).
        self.canva.bind('<Leave>',self.cursorquit) #The mouse pointer left the widget.
        self.canva.bind('<Button-1>',self.onLeftClick) #The left mouse button is pressed (use Button-2 for the middle button, Button-3 for the right button
        self.canva.bind('<B1-Motion>',self.onLeftClick)
        

        # When the left mouse button is released
        # self.canva.bind('<ButtonRelease-1>',self.add_to_old_draw)
        
        self.canva.bind('<B3-Motion>',self.onRightClick)
        self.canva.bind('<Button-3>',self.onRightClick)

        # Control + z
        self.bind("<Control-z>", self.undo)
        # Control + y
        self.bind("<Control-y>", self.redo)
        
        self.bind('<Configure>',self.resize)
        
        self.canva.place(x=290,y=120)

        # Set initial cursor to quill
        self.canva.config(cursor=self.custom_cursors['quill'])
    
    #======================Bind Init func=========================#

    #<<<<<<<Main window>>>>>>>
    def resize(self,event):
        """resize main window"""
        if event.widget == self:
            width=self.winfo_width() -310
            height=self.winfo_height() -140
                      
            self.width = width
            self.height = height
    
    #<<<<<<<Menu widget>>>>>>>
    def newpic(self):
        """create new ^picture with custom  size"""
        newpic = Newpic(self)
        newpic.grab_set()

    def loadpic(self):
        """load custom picture from folder"""
        self.filename=filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpg files",".jpg"),("png files",".png"),("all files",".")))
        self.picture['img']= Image.open(self.filename)

        self.picture['width'], self.picture['height'] = self.picture['img'].size
        self.canva["width"]=self.picture['width']
        self.canva["height"]=self.picture['height']

        self.filename=self.filename[:-4]

        self.refresh()

    def savepicas(self):
        """save actual picture under custom name/folder"""
        self.filename=filedialog.asksaveasfilename(initialdir = "/",title = "Select folder",filetypes = (("jpg files",".jpg"),("all files",".*")))
        self.picture['img'].save(self.filename+".jpg")

    def savepic(self):
        """save picture under same name if already saved / opened"""
        try :
            self.picture['img'].save(self.filename+".jpg")
        except : 
            self.filename=filedialog.asksaveasfilename(initialdir = "/",title = "Select folder",filetypes = (("jpg files",".jpg"),("all files",".*")))
            self.picture['img'].save(self.filename+".jpg")
    
    def clearcanva(self):
        """clear image"""
        self.old_draw.append(self.picture['img'].copy())

        self.picture['img']=Image.new('RGB',(self.picture['width'], self.picture['height']),(255,255,255))
        self.refresh()

        # Clear the new_draw list
        self.new_draw = []

    def convertASCII(self):
        """convert actual image / custom image into ASCII art"""
        self.picture['img'].save('asciiart.jpg')
        AsciiArt()
    
    #<<<<<<<Color palette>>>>>>>
    def selectcolor(self,event):
        """open color palette selection"""
        color = colorchooser.askcolor()[1]  # Retourne un tuple (couleur sélectionnée, code hexadécimal)
        if color:
            self.color = utility.HexToDec(color)
            self.colorL["text"]= color
        
    #<<<<<<<Main canva>>>>>>>
    def refresh(self):
        """diplay new image into canva after modification"""
        img_tk=ImageTk.PhotoImage(self.picture['img'])
        x=int(self.picture['width']/2)
        y=int(self.picture['height']/2)

        self.canva.create_image(x,y,image=img_tk)
        self.canva.image=img_tk

    def cursormove(self,event):
        """add circle making cursor size visible when quill tool enabled"""
        if self.actualtool=="quill":
            cursize = int(self.quillsize.get()/2)
            #create cursor
            self.cursor[f"id{self.cursorCount}"] =self.canva.create_oval(event.x-cursize, event.y-cursize,event.x+cursize,event.y+cursize,outline="black")
            #remove old cursor
            try : self.canva.delete(self.cursor[f"id{self.cursorCount-1}"])
            except : KeyError
            self.cursorCount+=1
        if self.actualtool=="fill":
            #put personalized cursor
            pass
        
    def cursorquit(self,event):
        """delete circle cursor and its history when quitting the canva"""
        try :
            self.canva.delete(self.cursor[f"id{self.cursorCount-1}"])
            self.cursorCount=0
        except : KeyError
        
    def quilltool(self,event):
        """enable quill tool when clicking on quill button"""
        if self.actualtool!="quill":
            self.actualtool="quill"
            self.canva.config(cursor=self.custom_cursors['quill'])

    def filltool(self, event):
        """enable fill tool when clicking on fill button"""
        if self.actualtool!="fill":
            self.actualtool="fill"
            self.canva.config(cursor=self.custom_cursors['fill'])

    def onLeftClick(self,event):
        """trace / fill into canva depeding of actual tool enabled"""

        self.old_draw.append(self.picture['img'].copy())

        #Main canva ---> quill
        if self.actualtool=="quill":
            #create shape at cursor
            cursize = int(self.quillsize.get()/2)
            self.picture['img']=modify_picture.modify_picture(self.picture['img'], self.color, event.x, event.y, cursize, self.picture['width'], self.picture['height'])
            self.refresh()

            # Clear the new_draw list
            self.new_draw = []

        #Main canva ---> fill
        if self.actualtool=="fill":
            self.picture['img'] = remplissage.modify_fill(self.picture['img'],event.x,event.y,self.color)
            self.refresh()
   
    def onRightClick(self, event):
        """erase in canva if quill tool enabled"""

        #Main canva ---> erase
        if self.actualtool=="quill":
            self.old_draw.append(self.picture['img'].copy())
            cursize = int(self.quillsize.get()/2)
            
            #newversion (editing img var)
            self.picture['img']=modify_picture.modify_picture(self.picture['img'], (255,255,255), event.x, event.y, cursize, self.picture['width'], self.picture['height'])
            self.refresh()
        
            #create cursor
            self.cursor[f"id{self.cursorCount}"] =self.canva.create_oval(event.x-cursize, event.y-cursize,event.x+cursize,event.y+cursize,outline="black")
            
            #remove old cursor
            try : self.canva.delete(self.cursor[f"id{self.cursorCount-1}"])
            except : KeyError
            self.cursorCount+=1

    #<<<<<<<Undo / Redo>>>>>>>
    def undo(self, event):
        """undo command for tkinter bind link"""
        self.undo_command()

    def undo_command(self):
        """undo command for tkinter command= link"""
        if self.old_draw:
            # Append the popped image to the new_draw list
            img_append = self.picture['img'].copy()
            self.new_draw.append(img_append)

            pop_img = self.old_draw.pop()
            self.picture['img'] = pop_img
            self.refresh()

    def redo(self, event):
        """redo command for tkinter bind link"""
        self.redo_command()

    def redo_command(self):
        """redo command for tkinter command= link"""
        if self.new_draw:
            # Append the popped image to the old_draw list
            img_append = self.picture['img'].copy()
            self.old_draw.append(img_append)

            pop_img = self.new_draw.pop()
            self.picture['img'] = pop_img
            self.refresh()

        
#==========================pop up============================#

class Newpic(tk.Toplevel):
    """create a popup for creation of a new picture"""
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent

        self.geometry('500x200')
        self.title('New picture')
        self.resizable(False,False)
        
        #Widgets
        self.WidthL = tk.Label(self,text="Width :")
        self.EntWidth = tk.Entry(self)
        self.pxL1 = tk.Label(self,text="px")
        self.WidthL.place(x=10,y=25)
        self.EntWidth.place(x=80,y=25,width=50)
        self.pxL1.place(x=135,y=25)
        self.EntWidth.focus()
    
        self.HeightL = tk.Label(self,text="Height :")
        self.EntHeight = tk.Entry(self)
        self.pxL2 = tk.Label(self,text="px")
        self.HeightL.place(x=170,y=25)
        self.EntHeight.place(x=240,y=25,width=50)
        self.pxL2.place(x=295,y=25)
        
        self.CancelB = tk.Button(self,text='Cancel',command=self.destroy)
        self.CancelB.place(x=180,y=120)
        self.CreateB = tk.Button(self,text='Create')
        self.CreateB.bind('<Button-1>',self.createCanva)
        self.CreateB.place(x=280,y=120)

    #Func        
    def createCanva(self,event):
        self.parent.picture['width']=int(self.EntWidth.get())
        self.parent.picture['height']=int(self.EntHeight.get())
        self.parent.canva["width"]=self.parent.picture['width']
        self.parent.canva["height"]=self.parent.picture['height']
        self.parent.picture['img']= Image.new('RGB',(self.parent.picture['width'], self.parent.picture['height']),(255,255,255))
        #to replace by destroying the matrice in the future
        self.parent.canva.delete("all")
        self.destroy()
        

app = Paint()
app.mainloop()