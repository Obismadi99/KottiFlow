import skia
from IPython.display import display, Image
from PIL import Image 

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import numpy as np

import time
import keyboard

#import thread
#import cv2 as cv


##############
# Parameters #
##############

MAT_WIDTH = 32 # width of pixel matrix
MAT_HEIGHT = 96 # height of pixel matrix
MIN_FRAME_TIME = 0.01667 # 60Hz are sufficient, so frame time doesn't have to be shorter than this (in seconds)

###########
# Classes #
###########

# Render Arrows flowing upward
class arrowsRenderer:
    currentOffset = 0

    def __init__(self, canvas, arrowHeight, arrowWidth, totalHeight, totalWidth):
        self.canvas = canvas
        self.arrowHeight = arrowHeight
        self.arrowWidth = arrowWidth
        #self.arrowDistance = arrowDistance
        #self.arrowProportion = arrowProportion  # [0.0, 1.0] - larger values make pointier arrows
        self.totalHeight = totalHeight
        self.totalWidth = totalWidth


    def drawArrow(self, posX, posY, color, arrowProportion):
        # configure paint
        paint = skia.Paint(
            AntiAlias = True,
            Color = skia.ColorBLACK,
            Style = skia.Paint.kFill_Style,
            StrokeWidth = 0,
            Shader = skia.GradientShader.MakeLinear(
                points = [(0.0, posY), (0.0, posY + self.arrowHeight)],
                colors = [color, skia.ColorBLACK]
            )
        )
        
        # create path
        path = skia.Path()
        
        #     y     y_tip
        #   /   \
        #  y     y  y_corner
        #  |     |
        #  y-----y  y_tail

        # intermediate values for better readability
        y_tip = posY
        y_corner = posY + arrowProportion*self.arrowHeight - 1.0
        #y_3 = posY + (1.0-arrowProportion)*self.arrowHeight
        y_tail = posY + self.arrowHeight

        x_left = posX
        x_center = posX + self.arrowWidth/2.0 - 0.5
        x_right = posX + self.arrowWidth

        path.moveTo(x_center, y_tip) # arrow tip

        path.lineTo(x_right, y_corner) # right edge upper
        path.lineTo(x_right, y_tail) # right edge lower
        
        #path.lineTo(x_center, y_corner) # tail middle

        path.lineTo(x_left, y_tail) # left edge lower
        path.lineTo(x_left, y_corner) # left edge upper

        path.lineTo(x_center, y_tip) # back to arrow tip

        #draw path
        self.canvas.drawPath(path, paint)

    def renderStep(self, incr, color, arrowProportion, arrowDistance):
        #increment offset and draw new arrows top to bottom
        self.currentOffset += incr
        if self.currentOffset >= arrowDistance:
            self.currentOffset -= arrowDistance

        currentY = -self.currentOffset # have to use negative value as arrows are moving bottom to top
        while currentY < self.totalHeight:
            self.drawArrow(0, currentY, color, arrowProportion)
            currentY += arrowDistance

# main renderer class, responsible for rendering the entirity of visuals,
# as well as displaying them in a preview window and/or outputting them to the LED matrix
class radbahnRenderer:

    frameTime = MIN_FRAME_TIME # keep track of frame time. init to a nonzero value.


    # TODO: determine interface with traffic light information. e.g. there have to be delays between state changes 
    # (doesn't make sense for the animation to change simultaneously with the traffic light itself) 
    #tl_phase = 'red' # should be kept in either 'red' or 'green'
    #tl_phase
    anim_state = 'green' # state of animation, should be either 'green' or 'red'
    anim_intensity = 0.0 # intensity of animation, should be inversely mapped to remaining time, perhaps not linear.  

    def __init__(self, preview: bool):
        #create drawing surface
        self.array = np.zeros((MAT_HEIGHT, MAT_WIDTH, 4), dtype=np.uint8)
        self.surface = skia.Surface(self.array)

        #create arrow renderer (draws arrows going up)
        self.arrows = arrowsRenderer(self.surface.getCanvas(), 0.7*MAT_WIDTH, MAT_WIDTH, MAT_HEIGHT, MAT_WIDTH)

        self.preview = preview # if true, display a preview window


    def updateImage(self):
        plt.clf()
        imgplot = plt.imshow(self.array)
        plt.pause(0.01)

    def calcAnimParams(self):
        #incr should be chosen wisely but im not wise right now
        incr = (0.5*self.anim_intensity + 0.1)*MAT_HEIGHT*self.frameTime #TODO have no clue if this makes sense, check when less tired
        color = skia.Color(int(255*self.anim_intensity), int(255*(1-self.anim_intensity)), 0)
        arrowDistance = 0.5*MAT_WIDTH # lazy, but could be changed for higher speeds
        arrowProportion = 0.2+self.anim_intensity
        return incr, color, arrowDistance, arrowProportion

    def renderFrame(self):
        #measure frame time (INCLUDING preview, and all other operations)
        t_start = time.time()

        # determine the actual parameters for the frame drawing functions from animation intensity value and previous frame time
        # when frametime is too long: must speed up animation. animation speed should depend on real time, not frame time.  
        #TODO
        incr, color, arrowDistance, arrowProportion = self.calcAnimParams()
        #color = skia.ColorGREEN

        # render new frame
        self.surface.getCanvas().clear(skia.ColorBLACK)
        self.arrows.renderStep(incr, color, arrowProportion, arrowDistance)

        if self.preview:             
            self.updateImage()

        # Write image to LED matrix
        # TODO

        t_done = time.time()
        # if frame time < minimum, just wait the difference.
        t_remain = MIN_FRAME_TIME - (t_done - t_start) # minimum frame time minus elapsed time = wait time 
        if (t_remain > 0):
            time.sleep(t_remain)

        self.frameTime = time.time() - t_start # store total frame time of this function call 
        print("frame time: "+str(self.frameTime))

    

def main():
    renderer = radbahnRenderer(preview=True)   
    plt.show()


    #i = 0
    while True:
        renderer.renderFrame()

        #TODO: renderer parameters (intensity, state) should be set here, i guess
        # --> need interface to traffic light
        
        #image = surface.makeImageSnapshot()
        #image.save('frame.png', skia.kPNG)
        
        renderer.anim_intensity += 0.01

        if (renderer.anim_intensity >= 1.0):
            renderer.anim_intensity = 0.0


if __name__ == '__main__':
    main()  