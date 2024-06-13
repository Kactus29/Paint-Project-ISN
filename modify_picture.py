import numpy as np
from PIL import Image, ImageTk

def sqrt(x): 
    return x**(1/2)
            

def modify_trace(img,color,x,y,pensize,canvawidth,canvaheight):
    """
    Parameters
    ----------
    img: 2D array filled with RGB tuples
    color : tuple (R,G,B)
    x: 0-canvawidth
    y: 0-canvaheight
    pensize: int
    
    ----------
    return: img modified (array)
    """
    pixels = img.load()
    canvaheight=int(canvaheight)
    canvawidth=int(canvawidth)
    #==========setting up boundaries
    #pensize=int(pensize/2) #penradius

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

def modify_fill(img, x, y, color):
    """
    Remplit une zone d'une image avec une nouvelle couleur en utilisant l'algorithme de remplissage par diffusion.

    Parameters:
    img (PIL.Image.Image): L'image à modifier.
    x (int): La coordonnée x du point de départ pour le remplissage.
    y (int): La coordonnée y du point de départ pour le remplissage.
    color (tuple): La nouvelle couleur sous forme de tuple RGB (R, G, B).

    Returns:
    PIL.Image.Image: L'image modifiée avec la zone remplie par la nouvelle couleur.

    Example:
    >>> from PIL import Image
    >>> img = Image.open('path_to_image.png')
    >>> new_img = modify_fill(img, 50, 50, (255, 0, 0))
    >>> new_img.show()
    """

    # Récupère les dimensions de l'image
    width, height = img.size

    # Convertit la nouvelle couleur en tuple (au cas où ce ne serait pas déjà le cas)
    new_color = tuple(color)

    # Récupère la couleur originale à la position de départ (x, y)
    original_color = img.getpixel((x, y))

    # Si la couleur originale est déjà la nouvelle couleur, ne fait rien
    if original_color == new_color:
        return img

    # Convertit l'image en tableau numpy pour un accès rapide aux pixels
    pixels = np.array(img)

    # Initialise une pile avec le point de départ
    stack = [(x, y)]
    
    # Boucle de remplissage par diffusion
    while stack:
        # Récupère les coordonnées actuelles de la pile
        cx, cy = stack.pop()

        # Vérifie si le pixel actuel correspond à la couleur originale
        if np.array_equal(pixels[cy, cx][:3], original_color):
            # Change la couleur du pixel actuel en la nouvelle couleur
            pixels[cy, cx] = new_color
            
            # Ajoute les pixels adjacents à la pile pour vérification future
            if cx > 0:
                stack.append((cx - 1, cy))
            if cx < width - 1:
                stack.append((cx + 1, cy))
            if cy > 0:
                stack.append((cx, cy - 1))
            if cy < height - 1:
                stack.append((cx, cy + 1))
    
    # Crée une nouvelle image à partir du tableau numpy modifié
    new_img = Image.fromarray(pixels)

    # Retourne l'image modifiée
    return new_img
