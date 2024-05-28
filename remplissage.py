# Dépendances 
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt



def flood_fill(edges : np.ndarray , x : int, y : int) -> list :
    
    
    Description : Prends en entrée une image edge detectionée et des coordonées initiales.
                  Renvoie une liste de tuples contenant les pixels à colorer

    Inputs : - edges (np.ndarray) : l'image binarisée avec un edge detection (avec Canny de cv2)
             - x (int) : La cordonée en x du point de départ
             - y (int) : La cordonée en x du point de départ

    Output : - liste_pixels_a_remplir (liste) : une liste des pixels qui doivent être remplis
    

    liste_pixels_a_remplir = set()  # Pour stocker les pixels déjà remplis
    stack = [(x, y)]  # Pile pour le remplissage par diffusion

    while stack:
        current_x, current_y = stack.pop()
        liste_pixels_a_remplir.add((current_x, current_y))

        # Ajoute les pixels voisins non remplis
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = current_x + dx, current_y + dy
            if (
                0 <= new_x < len(edges)
                and 0 <= new_y < len(edges[0])
                and (new_x, new_y) not in liste_pixels_a_remplir
                and edges[new_x][new_y] == 0
            ):
                stack.append((new_x, new_y))

    return list(liste_pixels_a_remplir)



def colorie_pixels(image : np.ndarray, liste_pixels : list, couleur : list) :
    
    
    Description : Prends en entrée une image, la liste des pixels à colorier ainsi que la couleur.
                  Colorie les pixels de la liste des pixels de la couleur indiquée

    Inputs : - image (np.ndarray) : l'image binarisée avec un edge detection (avec Canny de cv2)
             - liste_pixels (liste) : Une liste de tuples contenant des coordonées de pixels à colorer
             - couleur (liste) : Une liste contenant le code rgb d'une couleur (ex : [120,205,117])

    Output : Ne renvoie rien, modifie l'image directement
    

    for x,y in liste_pixels :
        image[x][y] = couleur


if __name__ == "__main__":

    image = cv2.imread('Test.png')
    edges = cv2.Canny(image=image, threshold1=100, threshold2=200)

    plt.figure(figsize=(20,10))
    plt.imshow(image)
    plt.show()

    liste = flood_fill(edges, 200, 200)

    colorie_pixels(image, liste, [0, 0, 254])

    plt.figure(figsize=(20,10))
    plt.imshow(image)
    plt.show()

"""

from PIL import Image, ImageDraw

def flood_fill(edges, x, y):
    """
    Description : Prend en entrée une image edge detectée et des coordonnées initiales.
                  Renvoie une image PIL avec le remplissage effectué.

    Inputs : - edges (Image) : l'image binarisée avec un edge detection
             - x (int) : La coordonnée x du point de départ
             - y (int) : La coordonnée y du point de départ

    Output : - filled_img (Image) : l'image avec le remplissage effectué
    """
    width, height = edges.size
    visited = set()
    stack = [(x, y)]

    # Créer une copie de l'image pour effectuer le remplissage
    filled_img = edges.copy()
    draw = ImageDraw.Draw(filled_img)

    while stack:
        x, y = stack.pop()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if 0 <= x < width and 0 <= y < height and edges.getpixel((x, y)) == 0:
            draw.point((x, y), fill=255)  # Remplir le pixel
            stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

    return filled_img

