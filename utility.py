from PIL import Image, ImageTk

def load_icon(img_path) :
    image = Image.open(img_path) #mjpg & png works
    image = image.resize((30, 30))
    image = ImageTk.PhotoImage(image) 
    return image

def HexToDec(hex):
    hex=hex[1:]
    R,G,B=hex[0:2],hex[2:4],hex[4:6]
    return (int(R,16),int(G,16),int(B,16))