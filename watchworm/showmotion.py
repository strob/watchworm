from util import VideoWriter, VideoReader, get_fps
import numpy
import cv2
import pickle
from jsonification import motion # this should be elsewhere ...
from ruledcontour import getRule # "" ""

def showmotion(src, paths, dest):
    FPS = get_fps(src)

    paths = pickle.load(open(paths))

    CROP = getRule('crop', src)

    # divide by number of frames
    # px/second
    avg_speeds = [FPS*motion(y)/(paths[idx][0][-1][4]-paths[idx][0][0][4]) for idx,(x,y) in enumerate(paths)]
    avg_speed = sum(avg_speeds) / len(avg_speeds)

    fr = None

    for idx,fr in enumerate(VideoReader(src)):
        if CROP > 0:
            fr = fr[CROP:-CROP,CROP:-CROP]

        if idx == 0:
            vout = VideoWriter(dest)

        speeds = []

        for p_idx,(raw,smooth) in enumerate(paths):
            raw = filter(lambda x: x[4] <= idx, raw)
            smooth = smooth[:max(0,len(raw)-5)]

            raw = numpy.array(raw)
            pts = raw[:,:2].astype(numpy.int32)
            cv2.polylines(fr, [pts], False, (255, 0, 0))

            tup = tuple(raw[-1,:2].astype(int).tolist())
            cv2.circle(fr, tup, raw[-1,2].astype(int), (255, 0, 0))
            cv2.circle(fr, tup, 3, (255, 0, 0))

            speed = 0
            if len(pts) > 1:
                speed = FPS*numpy.hypot(*(pts[-1] - pts[-2]).T)
            speeds.append(speed)
            txt = "%.2f (%.2f)" % (avg_speeds[p_idx], speed)
            cv2.putText(fr, txt, tup, cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0))

            # & smoothed
            if len(smooth) > 0:
                pts = numpy.array(smooth).astype(numpy.int32)
                cv2.polylines(fr, [pts], False, (0, 0, 255))
                
                tup = tuple(pts[-1].astype(int).tolist())
                cv2.circle(fr, tup, 3, (0, 0, 255))

            txt = "%.2f (%.2f), N=%d" % (avg_speed, sum(speeds)/len(speeds), len(paths))
            cv2.putText(fr, txt, (30,30), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255))

            vout.write(fr)            

if __name__=='__main__':
    import sys
    showmotion(*sys.argv[1:])
