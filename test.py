#!/usr/bin/env python
from samplebase import SampleBase
import time


class Test(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.parser.add_argument("-d", "--duration", help="The time (s) it takes to delete 1 row", default=0.1, type=float)

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        duration = self.args.duration

        while True:
            for i in range(self.matrix.height):
                for x in range(0, self.matrix.height):
                    for y in range(0, self.matrix.width):
                        if x >= i:
                            offset_canvas.SetPixel(x, y, 0, 255, 0)
                        else:
                            offset_canvas.SetPixel(x, y, 0, 0, 0)
                time.sleep(duration)
                offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

# Main function
if __name__ == "__main__":
    test = Test()
    if (not test.process()):
        test.print_help()
