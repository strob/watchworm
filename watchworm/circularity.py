import cv2
import numpy as np
import pickle
from quantification import *
from util import np2image

def getPoints(path):
    path = np.array(path)[:,:2]
    theta = angles(path)
    d_theta = abs(theta[1:] - theta[:-1])

    mags = np.hypot(*(path[1:] - path[:-1]).T)

    pts = [(0,0)]
    for M,THETA in zip(mags, d_theta):
        dx = M * np.cos(THETA)
        dy = M * np.sin(THETA)

        pts.append([pts[-1][0]+dx,
                    pts[-1][1]+dy])

    return np.array(pts)

def draw(path):
    pts = getPoints(path).astype(int)
    
    pts -= pts.min(axis=0)

    w,h = pts.max(axis=0)

    out = np.zeros((h,w,3), np.uint8)

    for idx,pt in enumerate(pts[:-1]):
        cv2.line(out, tuple(pt), tuple(pts[idx+1]), (0,255,0))

    return out

def circularity(paths, dest):
    paths = pickle.load(open(paths))
    ims = [draw(smooth) for raw,smooth in paths]
    sizes = np.array([[x.shape[1], x.shape[0]] for x in ims])
    w = sizes[:,0].max()
    h = sizes[:,1].sum()
    out = np.zeros((h,w,3), np.uint8)

    cury = 0
    for im in ims:
        out[cury:cury+im.shape[0],:im.shape[1]] = im
        cury += im.shape[0]

    np2image(out, dest)

if __name__=='__main__':
    import sys
    circularity(*sys.argv[1:])
