#!/usr/bin/env python
from samplebase import SampleBase

import numpy as np
from time import sleep

class Test(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--t-refresh", help="The time (s) it takes to refresh the LED matrix", default=0.01, type=float)
        self.parser.add_argument("--triangle-width", help="The number of pixels making one triangle in width direction", default=32, type=int)
        self.parser.add_argument("--triangle-height-min", help="The minimum number of pixels making one triangle in height direction", default=20, type=int)
        self.parser.add_argument("--n-reshape-triangle", help="The number of time intervalls t_refresh, between a change of the triangles' height", default=10, type=int)
    
    def updateColour(self, colour_param):
        if colour_param <= 0.5:
            green = int(2*colour_param*255)
            red = int(255)
        else:
            green = int(255)
            red = int(2*(1-colour_param)*255)
        self.colour = [red, green, 0]
    
    def generateGrids(self, grid_width, grid_height, triangle_width, triangle_height_min):
        triangle_height_diff_max = grid_height - triangle_height_min + 1
        self.arrays = np.zeros([triangle_height_diff_max, grid_width, grid_height, 3], dtype=np.uint8)
        
        for triangle_height_diff in range(triangle_height_diff_max):
            triangle_height = triangle_height_min + triangle_height_diff
            colour_param = triangle_height_diff/(grid_height - triangle_height_min)
            self.updateColour(colour_param)
            colour = self.colour
            
            for w in range(grid_width):
                h1= (w%triangle_width)*triangle_height/(2*triangle_width)
                h_min = (grid_height-triangle_height)/2 + h1
                h_max = (grid_height-1) - h_min
                brightness = (w%triangle_width)/(triangle_width-1)
                for h in range(grid_height):
                    if h >= h_min and h <=h_max:
                        self.arrays[triangle_height_diff, w, h, :] = [int(c*brightness) for c in  colour]
    
    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        
        # Geometric Parameters
        grid_width = self.matrix.width
        grid_height = self.matrix.height
        triangle_width = self.args.triangle_width
        triangle_height_min = self.args.triangle_height_min
        
        # Dynamic Parameters
        t_refresh = self.args.t_refresh
        n_change_triangle_height_max = self.args.n_reshape_triangle
        
        
        # Intitialisation
        offset = 0
        n_change_triangle_height= 0
        triangle_height_diff = 0
        triangle_height_diff_max = grid_height - triangle_height_min + 1
        
        # Generation of all possible pictures
        self.generateGrids(grid_width, grid_height, triangle_width, triangle_height_min)
        
#         print(self.arrays[triangle_height_diff_max-1, 0:32, 15,:])
        
        while True:
            for x in range(0, grid_width):
                    for y in range(0, grid_height):
                        offset_canvas.SetPixel((x+offset)%grid_width, y, self.arrays[triangle_height_diff, x, y, 0], self.arrays[triangle_height_diff, x, y, 1], self.arrays[triangle_height_diff, x, y, 2])

            offset += 1
            if offset == grid_width:
                offset = 0

            n_change_triangle_height += 1
            if n_change_triangle_height == n_change_triangle_height_max:
                triangle_height_diff +=1
                if triangle_height_diff == triangle_height_diff_max:
                    triangle_height_diff = 0
                n_change_triangle_height= 0
                
            sleep(t_refresh)
            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

# Main function
if __name__ == "__main__":
    test = Test()
    if (not test.process()):
        test.print_help()

