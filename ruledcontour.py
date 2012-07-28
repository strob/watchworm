import cv2
from cvframes import video_frames
from numpy import array, uint8, zeros, save
from numm import np2image
from numm.video import VideoWriter
import json
import pickle
import os

RULES = json.load(open('RULES.json'))
def getRule(key, src):
    return RULES.get(os.path.basename(src), RULES["default"]).get(key, RULES["default"][key])

def contours(src, dst):
    acc = []
    video = None
    vfr = None

    BLUR = getRule("blur", src)
    DILATION = getRule("dilation", src)
    THRESH = getRule("threshold", src)
    REVERSED = getRule("reversed", src)
    MERGE = getRule("merge", src)
    CROP = getRule("crop", src)

    merge = []

    for idx,fr in enumerate(video_frames(src, height=None)):
        if CROP > 0:
            fr = fr[CROP:-CROP,CROP:-CROP]

        if len(merge) >= MERGE:
            merge.pop(0)
        
        merge.append(fr.mean(axis=2).astype(int))

        fr = (array(merge).sum(axis=0) / len(merge)).astype(uint8)
        if REVERSED:
            fr = 255 - fr
        if BLUR > 0:
            cv2.blur(fr, (BLUR, BLUR), fr)

        if idx == 0:
            save("r1.npy", fr)

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
