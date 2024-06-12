import numpy as np
from PIL import Image, ImageTk

def sqrt(x): 
    return x**(1/2)
            

def modify_picture(img,color,x,y,pensize,canvawidth,canvaheight):
    """
    Parameters
    ----------
    img:2D array filled with RGB tuples
    color : tuple (R,G,B)
    x:0-canvawidth
    y:0-canvaheight
    pensize:int
    
    ----------
    return: img modified (array)
    """
    pixels = img.load()
    canvaheight=int(canvaheight)
    canvawidth=int(canvawidth)
    #==========setting up boundaries
    #pensize=int(pensize/2) #penradius
    
    # Simplier to understand version

    Xmin,Ymin,Xmax,Ymax=x-pensize,y-pensize,x+pensize,y+pensize
    if x-pensize<0:
        Xmin=0
    if y-pensize<0:
        Ymin=0
    if x+pensize>canvawidth:
        Xmax=canvawidth-1
    if y+pensize>canvaheight:
        Ymax=canvaheight-1

    #===========modification of img object

    for i in range (Ymin,Ymax+1):
        for j in range(Xmin,Xmax+1):
            
            #distance from center calculation
            if j==x : dist_from_center=0 
            elif i==y : dist_from_center=0 
            else : 
                if i > y :
                    if j > x :
                        dist_from_center = sqrt((i-y)**2+(j-x)**2)
                    else :
                        dist_from_center = sqrt((i-y)**2+(x-j)**2)
                else :
                    if j > x :
                        dist_from_center = sqrt((y-i)**2+(j-x)**2)
                    else :
                        dist_from_center = sqrt((y-i)**2+(x-j)**2)            
            
            #replace color if in range
            if dist_from_center < pensize or x==j and y==i:
                try : pixels[j,i]=color
                except IndexError : pass
            
    return img
                
"""
#test function :
xlen=300
ylen=300

img= Image.new('RGB', (xlen, ylen),(255,255,255))      
  
img = modify_picture(img, (128,0,128), 150,150, 50, xlen, ylen)
img.save("test_image.png")

import tkinter as tk

root = tk.Tk()
root.geometry('600x600')

canvas1 = tk.Canvas( root, width = 400, height = 400, bg="gray") 
canvas1.pack() 


def render_img(img,xlen=xlen,ylen=ylen):
    for i in range(0,xlen+1):
        print("[ ",end="")
        for j in range(0,ylen+1):
            for l in range(0,3):
                print(f"{img[i][j][l]}",end="")
            print(end=" |")
        print(" ]")
   

# Display image 
img_tk = ImageTk.PhotoImage(img)
canvas1.create_image(150,150,image=img_tk)
canvas1.image = img_tk

root.mainloop()
"""