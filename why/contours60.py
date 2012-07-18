import cv2
from cvframes import video_frames
from numpy import uint8, zeros
from numm import np2image, image2np
from numm.video import VideoWriter
import pickle

BLUR = 2
THRESH = 60
ENHANCE_MOTION = 1.0
DILATION = 3

def contours(src, dst):
    acc = []
    video = None
    vfr = None

    comp = 255 - image2np(src + '.comp.png').mean(axis=2)

    for idx,fr in enumerate(video_frames(src, height=None)):

        fr = 255 - fr.mean(axis=2)
        fr = (fr - ENHANCE_MOTION*comp).clip(0,255)
        cv2.blur(fr, (BLUR, BLUR), fr)

        # fill dynamic range
        fr = fr-fr.min()
        if fr.max() > 0:
            fr *= (255.0/fr.max())

        fr = 255*(fr>THRESH).astype(uint8)

        fr = cv2.dilate(fr, None, iterations=DILATION)

        if idx == 0:
            video = VideoWriter(dst.replace('.pkl', '.webm'), fr.shape)
            vfr = zeros((fr.shape[0],fr.shape[1],3), uint8)
            np2image(fr, dst.replace('.pkl', '.png'))

        vfr[:] = fr.reshape((fr.shape[0],fr.shape[1],-1))
        video.write(vfr)

        contours, hierarchy = cv2.findContours(fr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        acc.append(contours)

    video.close()
    pickle.dump(acc, open(dst, 'w'))

if __name__=='__main__':

    import sys
    contours(sys.argv[1], sys.argv[-1])
