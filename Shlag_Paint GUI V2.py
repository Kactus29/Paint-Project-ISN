import tkinter as tk
from tkinter import filedialog, colorchooser
import numpy as np
from PIL import Image, ImageTk
import cv2

import render_color
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
        self.pensize=tk.DoubleVar()
        self.color=(0,0,0)
        self.cursor={}
        self.cursorCount = 0
        self.actualtool="pen"
        
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
        editMenu.add_command(label="Undo")
        editMenu.add_command(label="Redo")
        editMenu.add_command(label="Clear", command=self.clearcanva)
        editMenu.add_separator()
        editMenu.add_command(label="Convert ASCII into art", command=self.convertASCII)
        menubar.add_cascade(label="Edit", menu=editMenu)
        
        self.config(menu = menubar)
        
        #pen tool
        self.fillB=tk.Button(self,text="P",bg="lightgreen",fg='black',width=3,height=1)
        self.fillB.bind('<Button-1>',self.pentool)
        self.fillB.place(x=10,y=20)
        
        #size scale pen
        self.sizeL = tk.Label(self,text="Pen Size :")
        self.sizeL.place(x=110,y=25)
        
        self.scalePen = tk.Scale(self, orient='horizontal', from_= 0, to = 100,resolution=1, tickinterval=25, length=200,variable = self.pensize)
        self.scalePen.place(x=200,y=5)
        
        #fill tool
        self.fillB=tk.Button(self,text="F",bg="lightgrey",fg='black', width=3,height=1)
        self.fillB.bind('<Button-1>',self.filltool)
        self.fillB.place(x=60,y=20)

        #color canva
        self.colorL = tk.Label(self,text='#000000')
        self.colorL.place(x=20,y=90)
        
        self.colorB = tk.Button(self,text="C",bg="lightgrey",fg='black', width=3,height=1)
        self.colorB.bind('<Button-1>',self.selectcolor)
        self.colorB.place(x=450,y=20)

        """old
        self.colorCanva=tk.Canvas(self,width=252,height=252,bg="white") #color render to define
        self.colorCanva.bind('<Button-1>',self.selectcolor)
        self.colorCanva.bind('<B1-Motion>',self.selectcolor)
        self.colorCanva.bind('<ButtonRelease-1>',self.selectcolor)
        self.colorCanva.place(x=20,y=120)
        """

        #main canva
        self.canva=tk.Canvas(self,bg="white",width=self.picture['width'],height=self.picture['height'])
        
        self.canva.create_image(self.picture['width'],self.picture['height'],image=ImageTk.PhotoImage(self.picture['img'])) #<----------------------------last edit
        self.canva.image=ImageTk.PhotoImage(self.picture['img']) #<----------------------------last edit
        
        self.canva.bind('<Motion>',self.cursormove) #The mouse is moved, with mouse button 1 being held down (use B2 for the middle button, B3 for the right button).
        self.canva.bind('<Leave>',self.cursorquit) #The mouse pointer left the widget.
        self.canva.bind('<Button-1>',self.onclick) #The left mouse button is pressed (use Button-2 for the middle button, Button-3 for the right button
        self.canva.bind('<B1-Motion>',self.trace)
        

        # When the left mouse button is released
        # self.canva.bind('<ButtonRelease-1>',self.add_to_old_draw)
        
        self.canva.bind('<B3-Motion>',self.erase)
        self.canva.bind('<Button-3>',self.on_right_click)
        # self.canva.bind('<Button-1>',self.fill)

        # Control + z
        self.bind("<Control-z>", self.undo)
        # Control + y
        self.bind("<Control-y>", self.redo)
        
        self.bind('<Configure>',self.resize)
        
        self.canva.place(x=290,y=120)
    
    #======================Bind Init func=========================#

    #Main window
    def resize(self,event):
        if event.widget == self:
            width=self.winfo_width() -310
            height=self.winfo_height() -140
            """
            if self.width != width or self.height!=height :
                if width >= height :
                    self.canva["width"]=height
                    self.canva["height"]=height
                else :
                    self.canva["width"]=width
                    self.canva["height"]=width
            """
                      
            self.width = width
            self.height = height
    
    #Menu widget
    def newpic(self):
        newpic = Newpic(self)
        newpic.grab_set()

    def loadpic(self):
        self.filename=filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpg files",".jpg"),("png files",".png"),("all files",".")))
        self.picture['img']= Image.open(self.filename)

        self.picture['width'], self.picture['height'] = self.picture['img'].size
        self.canva["width"]=self.picture['width']
        self.canva["height"]=self.picture['height']

        self.filename=self.filename[:-4]

        self.refresh()

    def savepicas(self):
        self.filename=filedialog.asksaveasfilename(initialdir = "/",title = "Select folder",filetypes = (("jpg files",".jpg"),("all files",".*")))
        self.picture['img'].save(self.filename+".jpg")

    def savepic(self):
        try :
            self.picture['img'].save(self.filename+".jpg")
        except : 
            self.filename=filedialog.asksaveasfilename(initialdir = "/",title = "Select folder",filetypes = (("jpg files",".jpg"),("all files",".*")))
            self.picture['img'].save(self.filename+".jpg")
    
    def clearcanva(self):
        # Add the current image to the old_draw list
        self.old_draw.append(self.picture['img'].copy())

        self.picture['img']=Image.new('RGB',(self.picture['width'], self.picture['height']),(255,255,255))
        self.refresh()

        # Clear the new_draw list
        self.new_draw = []

    def convertASCII(self):
        AsciiArt()
    
    #Color canva
    def selectcolor(self,event):
        color = colorchooser.askcolor()[1]  # Retourne un tuple (couleur sélectionnée, code hexadécimal)
        if color:
            self.color = render_color.HexToDec(color)
            self.colorL["text"]= color

    """ old
    def selectcolor(self,event):
        x=event.x
        y=event.y
        factor = x/255
        
        if y<43 :
            R=0
            G=128-y*3
            B=127+y*3
        elif y>=43 and y<85:
            R=(y-43)*3
            G=0
            B=255-(y-43)*3
        elif y>=85 and y<128:
            R=128+(y-85)*3
            G=0
            B=128-(y-85)*3
        elif y>=128 and y<213 :
            R=255-(y-128)*3
            G=(y-128)*3
            B=0
        elif y>=213 and y<256 :
            R=0
            G=255-(y-213)*3
            B=(y-213)*3
        
        R=render_color.factorize(R,factor)
        G=render_color.factorize(G,factor)
        B=render_color.factorize(B,factor)
        

        self.RGB=(R,G,B)
        self.color= render_color.render_color_dechex(R,G,B,factor)

        self.colorCanva["bg"]=self.color
    """
        
        
    #Main canva
    def refresh(self):
        img_tk=ImageTk.PhotoImage(self.picture['img'])
        x=int(self.picture['width']/2)
        y=int(self.picture['height']/2)

        self.canva.create_image(x,y,image=img_tk)
        self.canva.image=img_tk


    def cursormove(self,event):
        if self.actualtool=="pen":
            cursize = int(self.pensize.get()/2)
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
        try :
            self.canva.delete(self.cursor[f"id{self.cursorCount-1}"])
            self.cursorCount=0
        except : KeyError
        
    #Main canva ---> pen
    def pentool(self,event):
        if self.actualtool!="pen":
            self.actualtool="pen"
    
    def trace(self, event): 
        if self.actualtool=="pen":
            #create shape at cursor
            cursize = int(self.pensize.get()/2)
            
            self.picture['img']=modify_picture.modify_picture(self.picture['img'], self.color, event.x, event.y, cursize, self.picture['width'], self.picture['height'])
            
            self.refresh()

    def onclick(self,event):
        self.old_draw.append(self.picture['img'].copy())

        if self.actualtool=="pen":
            #create shape at cursor
            cursize = int(self.pensize.get()/2)
            
            self.picture['img']=modify_picture.modify_picture(self.picture['img'], self.color, event.x, event.y, cursize, self.picture['width'], self.picture['height'])
            
            self.refresh()

            # Clear the new_draw list
            self.new_draw = []

        if self.actualtool=="fill":
            self.picture['img'] = remplissage.modify_fill(self.picture['img'],event.x,event.y,self.color)
            self.refresh()

    # def add_to_old_draw(self, event):
    #     if self.actualtool=="pen":
    #         self.old_draw.append(self.picture['img'].copy())

    #         #create shape at cursor
    #         cursize = int(self.pensize.get()/2)
            
    #         self.picture['img']=modify_picture.modify_picture(self.picture['img'], self.color, event.x, event.y, cursize, self.picture['width'], self.picture['height'])
            
    #         self.refresh()

    #         # Clear the new_draw list
    #         self.new_draw = []

    def undo(self, event):
        if self.old_draw:
            # Append the popped image to the new_draw list
            img_append = self.picture['img'].copy()
            self.new_draw.append(img_append)

            pop_img = self.old_draw.pop()
            self.picture['img'] = pop_img
            self.refresh()

    def redo(self, event):
        if self.new_draw:
            # Append the popped image to the old_draw list
            img_append = self.picture['img'].copy()
            self.old_draw.append(img_append)

            pop_img = self.new_draw.pop()
            self.picture['img'] = pop_img
            self.refresh()
        
    def on_right_click(self, event):
        if self.actualtool=="pen":
            self.old_draw.append(self.picture['img'].copy())
            cursize = int(self.pensize.get()/2)
            
            #newversion (editing img var)
            self.picture['img']=modify_picture.modify_picture(self.picture['img'], (255,255,255), event.x, event.y, cursize, self.picture['width'], self.picture['height'])
            self.refresh()
        
            #create cursor
            self.cursor[f"id{self.cursorCount}"] =self.canva.create_oval(event.x-cursize, event.y-cursize,event.x+cursize,event.y+cursize,outline="black")
            
            #remove old cursor
            try : self.canva.delete(self.cursor[f"id{self.cursorCount-1}"])
            except : KeyError
            self.cursorCount+=1
        
    def erase(self,event):
        if self.actualtool=="pen":
            cursize = int(self.pensize.get()/2)
            
            #newversion (editing img var)
            self.picture['img']=modify_picture.modify_picture(self.picture['img'], (255,255,255), event.x, event.y, cursize, self.picture['width'], self.picture['height'])
            self.refresh()
        
            #create cursor
            self.cursor[f"id{self.cursorCount}"] =self.canva.create_oval(event.x-cursize, event.y-cursize,event.x+cursize,event.y+cursize,outline="black")
            
            #remove old cursor
            try : self.canva.delete(self.cursor[f"id{self.cursorCount-1}"])
            except : KeyError
            self.cursorCount+=1

    #Main canva ---> fill
    def filltool(self, event):
        if self.actualtool!="fill":
            self.actualtool="fill"
        
    # def fill(self,event):
    #     if self.actualtool=="fill":
    #         self.picture['img'] = remplissage.modify_fill(self.picture['img'],event.x,event.y,self.color)
    #         self.refresh()

        
#=============================pop up=========================#

class Newpic(tk.Toplevel):
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