# compute paths from a contours pickle

import pickle
import cv2
import numpy
from util import image2np, np2image

MIN_AREA = 15
MAX_DIST = 0.1                  # percentage of area
SMOOTHING_WINDOW_LEN = 25

MIN_NFRAMES = 100               # Otherwise path is considered too-short.

def smooth(path):
    window = numpy.kaiser(SMOOTHING_WINDOW_LEN, 4)
    window = window / window.sum()
    y = numpy.convolve(path[:,0], window, mode='valid')
    x = numpy.convolve(path[:,1], window, mode='valid')

    # Include first and last point
    y = numpy.concatenate([[path[0,0]],y,[path[-1,0]]])
    x = numpy.concatenate([[path[0,1]],x,[path[-1,1]]])
    return numpy.array([y,x]).T

def path(src, dest):
    contours = pickle.load(open(src))

    paths = []

    for idx,clist in enumerate(contours):

        # center (x,y) / radius / area / frame index

        xyRAI = [[cv2.minEnclosingCircle(X), cv2.contourArea(X)] for X in clist]
        # unpack
        xyRAI = [[x[0][0][0],x[0][0][1],x[0][1],x[1],idx] for x in xyRAI]
        xyRAI = filter(lambda x: x[3] >= MIN_AREA, xyRAI)

        if idx == 0:
            for start in xyRAI:
                paths.append([start])

        lasts = numpy.array([X[-1] for X in paths])

        _matched = set()
        for ctr in xyRAI:
            dists = abs(lasts - ctr).mean(axis=1)
            if dists.min() < MAX_DIST*ctr[-2]:
                p_idx = dists.argmin()
                if p_idx in _matched:
                    opp = paths[p_idx].pop()
                    opp_dist = abs(numpy.array(paths[p_idx][-1]) - opp).mean()
                    my_dist = abs(numpy.array(paths[p_idx][-1]) - ctr).mean()

                    if my_dist < opp_dist:
                        # print 'warning: double match duel -- win!', my_dist, opp_dist
                        paths[p_idx].append(ctr)
                    else:
                        # print 'warning: double match duel -- lose :(', my_dist, opp_dist
                        paths[p_idx].append(opp)
                    continue

                _matched.add(p_idx)
                paths[p_idx].append(ctr)
            else:
                # Stray contour: make new and see what happens
                paths.append([ctr])

    # prune short paths
    paths = filter(lambda x: len(x) > MIN_NFRAMES, paths)

    # smooth paths
    smoothed = [smooth(numpy.array(X)) for X in paths]

    # print 'trimmed %d paths to %d' % (len(plens), len(paths))

    # save a preview PNG
    fr = 255 - image2np(dest.replace('path', 'contours').replace('.pkl', '.png'))
    for idx,path in enumerate(paths):
        path = numpy.array(path)[:,:2].astype(numpy.int32)
        cv2.polylines(fr, [path], False, (255, 0, 0))

        # & smoothed
        path = numpy.array(smoothed[idx]).astype(numpy.int32)
        cv2.polylines(fr, [path], False, (0, 0, 255))

    np2image(fr, dest.replace('.pkl', '.png'))

    pickle.dump(zip(paths, smoothed), open(dest, 'w'))

if __name__=='__main__':
    import sys
    path(sys.argv[1], sys.argv[-1])
