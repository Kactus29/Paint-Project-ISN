# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:16:19 2024

@author: sylva
"""

import tkinter as tk

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
        self.color="purple"
        self.cursor={}
        self.cursorCount = 0
        self.conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 
                    5: '5', 6: '6', 7: '7', 
                    8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 
                    13: 'D', 14: 'E', 15: 'F'} 
      
    #widget#
    def initwidget(self):
        #clear button
        self.clearB=tk.Button(self,text="Clear",bg="lightgreen")
        self.clearB.bind('<Button-1>',self.clearcanva)
        self.clearB.place(x=20,y=20)
        
        #size scale pen
        self.sizeL = tk.Label(self,text="Pen Size :")
        self.sizeL.place(x=100,y=25)
        
        self.scalePen = tk.Scale(self, orient='horizontal', from_= 0, to = 100,resolution=1, tickinterval=25, length=200,variable = self.pensize)
        self.scalePen.place(x=180,y=5)
        
        #color canva
        self.colorL = tk.Label(self,text=self.rendercolor(self.color))
        self.colorL.place(x=20,y=90)
        
        self.colorCanva=tk.Canvas(self,width=252,height=252,bg="white") #color render to define
        self.colorCanva.bind('<Button-1>',self.selectcolor)
        self.colorCanva.bind('<B1-Motion>',self.selectcolor)
        self.colorCanva.bind('<ButtonRelease-1>',self.selectcolor)
        self.colorCanva.place(x=20,y=120)
        
        #main canva
        self.canva=tk.Canvas(self,bg="white",width=420,height=420)
        self.canva.bind('<Motion>',self.cursormove) #The mouse is moved, with mouse button 1 being held down (use B2 for the middle button, B3 for the right button).
        self.canva.bind('<Leave>',self.cursorquit) #The mouse pointer left the widget.
        self.canva.bind('<B1-Motion>',self.trace)
        self.canva.bind('<Button-1>',self.trace)
        
        self.canva.bind('<B3-Motion>',self.erase)
        self.canva.bind('<Button-3>',self.erase)
        
        self.bind('<Configure>',self.resize)
        
        self.canva.place(x=290,y=120)
    
    #======================Bind Init func=========================#
    
    def rendercolor(self,color):
        return f"#{self.color}"
    
    def clearcanva(self,event):
        self.canva.delete("all")
    
    def factorize(self,x,factor):
        return int(x*factor)
  
    def decToHex(self,decimal): 
        hexadecimal = '' 
        while(decimal > 0): 
            remainder = decimal % 16
            hexadecimal = self.conversion_table[remainder] + hexadecimal 
            decimal = decimal // 16
            
        if len(hexadecimal)==1:
            hexadecimal ="0"+hexadecimal
        if len(hexadecimal)==0:
            hexadecimal ="00"
        return hexadecimal 
    
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
        
        R=self.factorize(R,factor)
        G=self.factorize(G,factor)
        B=self.factorize(B,factor)
        
        self.color= "#"+ self.decToHex(R)+self.decToHex(G)+self.decToHex(B)
        self.colorL["text"]= self.color
        self.colorCanva["bg"]=self.color
    
    def cursormove(self,event):
        cursize = int(self.pensize.get()/2)
        #create cursor
        self.cursor[f"id{self.cursorCount}"] =self.canva.create_oval(event.x-cursize, event.y-cursize,event.x+cursize,event.y+cursize,outline="black")
        #remove old cursor
        try : self.canva.delete(self.cursor[f"id{self.cursorCount-1}"])
        except : KeyError
        self.cursorCount+=1
        
    def cursorquit(self,event):
        self.canva.delete(self.cursor[f"id{self.cursorCount-1}"])
        self.cursorCount=0
        
        
    def trace(self, event): 
        #create shape at cursor
        cursize = int(self.pensize.get()/2)
        self.canva.create_oval(event.x-cursize, event.y-cursize,event.x+cursize,event.y+cursize,fill=self.color,outline=self.color)
        
        
    def erase(self,event):
        cursize = int(self.pensize.get()/2)
        
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
        

app = Paint()
app.mainloop()
