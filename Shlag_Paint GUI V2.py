# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:16:19 2024

@author: sylva
"""

import tkinter as tk
import numpy as np

import render_color
import modify_picture

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
        
        self.initvar()
        self.initwidget()
    
    #======================Sub func Init========================#
    
    #var#
    def initvar(self):
        self.pensize=tk.DoubleVar()
        self.color="000000"
        self.RGB=(0,0,0)
        self.cursor={}
        self.cursorCount = 0
        self.CanvaWidth=420
        self.CanvaHeight=420
        self.actualtool="pen"
        
        self.picture={'height':420,'width':420,'img':np.array(modify_picture.create_img(self.CanvaHeight, self.CanvaHeight))}
    
    #widget#
    def initwidget(self):
        #Menu
        menubar = tk.Menu(self)

        options = tk.Menu(menubar, tearoff = 0)
        options.add_command(label="New",command=self.newpic)
        options.add_command(label="Load")
        options.add_command(label="Save")
        options.add_separator()
        options.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=options)

        editMenu = tk.Menu(menubar, tearoff = 0)
        editMenu.add_command(label="Undo")
        editMenu.add_command(label="Redo")
        editMenu.add_command(label="Clear", command=self.clearcanva)
        editMenu.add_separator()
        editMenu.add_command(label="Convert ASCII into art")
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
        self.colorL = tk.Label(self,text=render_color.renderLabel(self.color))
        self.colorL.place(x=20,y=90)
        
        self.colorCanva=tk.Canvas(self,width=252,height=252,bg="white") #color render to define
        self.colorCanva.bind('<Button-1>',self.selectcolor)
        self.colorCanva.bind('<B1-Motion>',self.selectcolor)
        self.colorCanva.bind('<ButtonRelease-1>',self.selectcolor)
        self.colorCanva.place(x=20,y=120)
        
        #main canva
        self.canva=tk.Canvas(self,bg="white",width=self.CanvaWidth,height=self.CanvaHeight)
        self.canva.bind('<Motion>',self.cursormove) #The mouse is moved, with mouse button 1 being held down (use B2 for the middle button, B3 for the right button).
        self.canva.bind('<Leave>',self.cursorquit) #The mouse pointer left the widget.
        self.canva.bind('<B1-Motion>',self.trace)
        self.canva.bind('<Button-1>',self.trace)
        
        self.canva.bind('<B3-Motion>',self.erase)
        self.canva.bind('<Button-3>',self.erase)
        
        self.bind('<Configure>',self.resize)
        
        self.canva.place(x=290,y=120)
    
    #======================Bind Init func=========================#
    
    #Main window
    def resize(self,event):
        if event.widget == self:
            width=self.winfo_width() -310
            height=self.winfo_height() -140
            if self.width != width or self.height!=height :
                if width >= height :
                    self.canva["width"]=height
                    self.canva["height"]=height
                else :
                    self.canva["width"]=width
                    self.canva["height"]=width
                    
            self.width = width
            self.height = height
    
    #Menu widget
    def newpic(self):
        newpic = Newpic(self)
        newpic.grab_set()
    
    def clearcanva(self):
        self.canva.delete("all")
    
    #Color canva
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
        self.colorL["text"]= self.color
        self.colorCanva["bg"]=self.color
    
    #Main canva
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
        self.canva.delete(self.cursor[f"id{self.cursorCount-1}"])
        self.cursorCount=0
        
    #Main canva ---> pen
    def pentool(self,event):
        if self.actualtool!="pen":
            self.actualtool="pen"
    
    def trace(self, event): 
        if self.actualtool=="pen":
            #create shape at cursor
            cursize = int(self.pensize.get()/2)
            
            ##newversion (editing img var)
            modify_picture.modify_picture(self.picture['img'], self.RGB, event.x, event.y, cursize, self.CanvaWidth, self.CanvaHeight)
            
            ##old :
            self.canva.create_oval(event.x-cursize, event.y-cursize,event.x+cursize,event.y+cursize,fill=self.color,outline=self.color)
        
        
    def erase(self,event):
        if self.actualtool=="pen":
            cursize = int(self.pensize.get()/2)
            
            #newversion (editing img var)
            modify_picture.modify_picture(self.picture['img'], (0,0,0), event.x, event.y, cursize, self.CanvaWidth, self.CanvaHeight)
            
            ## old :
                
            #delete all others shapes
            ids_square = self.canva.find_overlapping(event.x-int(3/4*cursize), event.y-int(3/4*cursize), event.x+int(3/4*cursize), event.y+int(3/4*cursize))
            ids_vertical = self.canva.find_overlapping(event.x-int(3/16*cursize), event.y-cursize, event.x+int(3/16*cursize), event.y+cursize)
            ids_horizontal = self.canva.find_overlapping(event.x-cursize, event.y-int(3/8*cursize), event.x+cursize, event.y+int(3/8*cursize))
            ids=tuple(set(ids_square + ids_vertical + ids_horizontal))

        for id in ids :
            self.canva.delete(id)
        
        #create cursor
        self.cursor[f"id{self.cursorCount}"] =self.canva.create_oval(event.x-cursize, event.y-cursize,event.x+cursize,event.y+cursize,outline="black")
        
        #remove old cursor
        try : self.canva.delete(self.cursor[f"id{self.cursorCount-1}"])
        except : KeyError
        self.cursorCount+=1
    
    #Main canva ---> fill
    def filltool(self, event):
        if self.actualtool!="fill":
            pass
        
#=============================pop up=========================#

class Newpic(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent

        self.geometry('500x200')
        self.title('New picture')
        self.resizable(False,False)
        
        #Var
        self.CanvaWidth=0
        self.CanvaHeight=0
        
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
        self.parent.CanvaWidth=self.EntWidth.get()
        self.parent.CanvaHeight=self.EntHeight.get()
        self.parent.canva["width"]=self.parent.CanvaWidth
        self.parent.canva["height"]=self.parent.CanvaHeight
        self.parent.picture={'height':self.parent.CanvaHeight,'width':self.parent.CanvaWidth,'img':np.array(modify_picture.create_img(self.parent.CanvaHeight, self.parent.CanvaHeight))}
        #to replace by destroying the matrice in the future
        self.parent.canva.delete("all")
        self.destroy()
        
          
app = Paint()
app.mainloop()
