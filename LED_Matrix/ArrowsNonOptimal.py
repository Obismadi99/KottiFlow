#!/usr/bin/env python
from samplebase import SampleBase

import numpy as np
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

class Test(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--t-refresh", help="The time (s) it takes to refresh the LED matrix", default=0.02, type=float)
        self.parser.add_argument("--triangle-width", help="The number of pixels making one triangle in width direction", default=16, type=int)
        self.parser.add_argument("--triangle-height-min", help="The minimum number of pixels making one triangle in height direction", default=20, type=int)
    
    
    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        
        # Geometric Parameters
        grid_width = self.matrix.width
        grid_height = self.matrix.height
        triangle_width = self.args.triangle_width
        triangle_height_min = self.args.triangle_height_min
        
        # Dynamic Parameters
        t_refresh = self.args.t_refresh
        n_change_triangle_height_max = 10
        
        
        # Intitialisation
        offset = 0
        n_change_triangle_height= 0
        triangle_height_diff = 0
        
        while True:
            triangle_height = triangle_height_min + triangle_height_diff
            color_param = triangle_height_diff/(grid_height - triangle_height_min)
            color = calculate_color(color_param)
            LED_Matrix = create_LED_Matrix(grid_width, grid_height, triangle_width, triangle_height, offset, color)

            for x in range(0, grid_width):
                for y in range(0, grid_height):
                    offset_canvas.SetPixel(x, y, LED_Matrix[x, y, 0], LED_Matrix[x, y, 1], LED_Matrix[x, y, 2])


            offset += 1
            if offset == grid_width:
                offset = 0

            n_change_triangle_height += 1
            if n_change_triangle_height == n_change_triangle_height_max:
                triangle_height_diff +=1
                if triangle_height_diff == grid_height - triangle_height_min + 1:
                    triangle_height_diff = 0
                n_change_triangle_height= 0
                
            sleep(t_refresh)
            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

# Main function
if __name__ == "__main__":
    test = Test()
    if (not test.process()):
        test.print_help()

