import cv2
from cvframes import video_frames
from numpy import uint8
import pickle

BLUR = 2
# ???
A = 45
B = 45

DILATION = 3

def contours(src, dst):
    acc = []
    ADAPTIVE = True
    for idx,fr in enumerate(video_frames(src, height=None)):
        if idx == 0:
            if fr.mean() < 30:
                print 'Very dark: not attempting an adaptive threshold.'
                ADAPTIVE = False

        fr = fr.mean(axis=2)
        cv2.blur(fr, (BLUR, BLUR), fr)
        fr = fr.astype(uint8)
        if ADAPTIVE:
            fr = cv2.adaptiveThreshold(fr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, A, B)
        else:
            fr = 255*(fr>60).astype(uint8)

        fr = cv2.dilate(fr, None, iterations=DILATION)

        contours, hierarchy = cv2.findContours(fr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        acc.append(contours)

    pickle.dump(acc, open(dst, 'w'))

if __name__=='__main__':
    import sys
    contours(sys.argv[1], sys.argv[2])
