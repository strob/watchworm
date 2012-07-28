import numpy as np
import cv2
from watchworm.util import VideoWriter

def movingCircles(outfile, paths, size=(640,480), r=20, fps=30.0):
    vout = VideoWriter(outfile)
    for pts in zip(*paths):
        print pts
        fr = np.zeros((size[1],size[0],3), dtype=np.uint8)
        for pt in pts:
            cv2.circle(fr, pt, r, (255,255,255), -1)
        vout.write(fr)

if __name__=='__main__':
    import os
    if not os.path.isdir('data'):
        os.makedirs('data')

    # Make a path from (100,100) to (200,100) over 30 frames.
    x = np.linspace(100,200,30).astype(int)
    y = 100*np.ones(30).astype(int)

    movingCircles('data/circleAtSpeed100.avi', [zip(x,y)])

    # Add a second path that starts off-screen.
    x2 = np.linspace(680,580,30).astype(int)
    y2 = 200*np.ones(30).astype(int)

    movingCircles('data/offscreenCircles100.avi', [zip(x,y), zip(x2,y2)])
