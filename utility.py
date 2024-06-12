from PIL import Image, ImageTk

def load_icon(img_path) :
    """
    Parameters
    ----------
    img_path: str of filepath to image
    ----------
    return: image in format tkinter can use
    """
    image = Image.open(img_path) #mjpg & png works
    image = image.resize((30, 30))
    image = ImageTk.PhotoImage(image) 
    return image

def HexToDec(hex):
    """
    Parameters
    ----------
    hex: str of heximal number in color format (#)
    ----------
    return: tuple of decimal rgb color format (R,G,B)
    """
    hex=hex[1:]
    R,G,B=hex[0:2],hex[2:4],hex[4:6]
    return (int(R,16),int(G,16),int(B,16))