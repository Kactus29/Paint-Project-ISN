def HexToDec(hex):
    hex=hex[1:]
    R,G,B=hex[0:2],hex[2:4],hex[4:6]
    return (int(R,16),int(G,16),int(B,16))

"""
conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 
            5: '5', 6: '6', 7: '7', 
            8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 
            13: 'D', 14: 'E', 15: 'F'} 

def factorize(x,factor):
    return int(x*factor)

def decToHex(decimal): 
    hexadecimal = '' 
    while(decimal > 0): 
        remainder = decimal % 16
        hexadecimal = conversion_table[remainder] + hexadecimal 
        decimal = decimal // 16
        
    if len(hexadecimal)==1:
        hexadecimal ="0"+hexadecimal
    if len(hexadecimal)==0:
        hexadecimal ="00"
    return hexadecimal 

def render_color_dechex(R,G,B,factor) :
    R=factorize(R,factor)
    G=factorize(G,factor)
    B=factorize(B,factor)
    
    return "#"+ decToHex(R)+decToHex(G)+decToHex(B)

def renderLabel(color):
    return f"#{color}"
"""
