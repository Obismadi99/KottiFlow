import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from time import sleep

def create_LED_Matrix(grid_width, grid_height, triangle_width, triangle_height, offset, color):
    LED_Matrix = np.zeros([grid_width, grid_height, 3], dtype=np.uint8)
    for w in range(grid_width):
        h1= ((w-offset)%triangle_width)*triangle_height/(2*triangle_width)
        h_min = (grid_height-triangle_height)/2 + h1
        h_max = (grid_height-1) - h_min
        brightness = (w-offset)%(triangle_width)/(triangle_width-1)
        for h in range(grid_height):
            if h >= h_min and h <=h_max:
                LED_Matrix[w, h, :] = [int(c*brightness) for c in  color]
    return LED_Matrix

def calculate_color(color_param):
    if color_param <= 0.5:
        green = int(2*color_param*255)
        red = int(255)
    else:
        green = int(255)
        red = int(2*(1-color_param)*255)

    color = [red, green, 0]
    return color

# Geometric Parameters
grid_width = 96
grid_height = 32
triangle_width = 16
triangle_height_min = 20

# Dynamic Parameters
t_refresh = 0.02
n_move_arrow_max = 1
n_change_triangle_height_max = 10

# Tkinter Window creation
window = tk.Tk()  
canvas = tk.Canvas(window, width = 500, height = 500)  
canvas.pack()

# Intitialisation
n_move_arrow = 0
offset = 0
n_change_triangle_height= 0
triangle_height_diff = 0

try:
    while True:
        triangle_height = triangle_height_min + triangle_height_diff
        color_param = triangle_height_diff/(grid_height - triangle_height_min)
        color = calculate_color(color_param)
        LED_Matrix = create_LED_Matrix(grid_width, grid_height, triangle_width, triangle_height, offset, color)

        n_move_arrow += 1
        if n_move_arrow == n_move_arrow_max:
            offset += 1
            if offset == grid_width:
                offset = 0
            n_move_arrow = 0

        n_change_triangle_height += 1
        if n_change_triangle_height == n_change_triangle_height_max:
            triangle_height_diff +=1
            if triangle_height_diff == grid_height - triangle_height_min + 1:
                triangle_height_diff = 0
            n_change_triangle_height= 0

        # Draw LED Matrix
        img = Image.fromarray(LED_Matrix, mode='RGB')
        imgTk = ImageTk.PhotoImage(img.resize((150, 450)))
        canvas.create_image(250, 250, anchor ='center', image=imgTk) 
        window.update()

        
        sleep(t_refresh)

except KeyboardInterrupt:
    print('Exit')