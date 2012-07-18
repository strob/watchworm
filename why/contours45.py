import cv2
from cvframes import video_frames
from numpy import uint8
from numm import np2image
import pickle

BLUR = 2

# ???
A = 45
B = 45

DILATION = 3

def findBorder(fr):
    left = (fr[:50,fr.shape[2]/2].mean(axis=1)>50).argmax()
    return 2*left

def contours(src, dst):
    acc = []
    border = 0
    ADAPTIVE = True
    for idx,fr in enumerate(video_frames(src, height=None)):
        
        if idx == 0:
            if fr.mean() < 30:
                print 'Very dark: not attempting an adaptive threshold.'
                ADAPTIVE = False
            border = findBorder(fr)
            print 'border:', border

        fr = fr.mean(axis=2)
        cv2.blur(fr, (BLUR, BLUR), fr)
        fr = fr.astype(uint8)

        # fill dynamic range
        fr = fr-fr.min()
        if fr.max() > 0:
            fr *= (255.0/fr.max())

        if ADAPTIVE:
            fr[border:-border,border:-border] = cv2.adaptiveThreshold(fr[border:-border,border:-border], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, A, B)
        else:
            # This is a catch for the suppressor recordings, where target is white.
            fr = 255*(fr>60).astype(uint8)

        fr = cv2.dilate(fr, None, iterations=DILATION)

        if idx == 0:
            np2image(fr, dst.replace('.pkl', '.png'))

        contours, hierarchy = cv2.findContours(fr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        acc.append(contours)

    pickle.dump(acc, open(dst, 'w'))

if __name__=='__main__':
    import sys
    contours(sys.argv[1], sys.argv[2])
