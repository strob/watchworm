from cvframes import video_frames
from numm.video import VideoWriter
import numpy
import cv2
import pickle
from jsonification import motion # this should be elsewhere ...

def showmotion(src, paths, dest):
    paths = pickle.load(open(paths))

    # divide by number of frames
    avg_speeds = [motion(y)/paths[idx][-1][0][-1] for idx,(x,y) in enumerate(paths)]

    vout = None
    fr = None

    for idx,ofr in enumerate(video_frames(src, height=None)):
        if idx == 0:
            vout = VideoWriter(dest, ofr.shape)
            fr = numpy.zeros(ofr.shape, dtype=numpy.uint8)

        fr[:] = 255-ofr             # contiguity ...

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
                speed = numpy.hypot(*(pts[-1] - pts[-2]).T)
            txt = "%.2f (%.2f)" % (avg_speeds[p_idx], speed)
            cv2.putText(fr, txt, tup, cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0))

            # & smoothed
            if len(smooth) > 0:
                pts = numpy.array(smooth).astype(numpy.int32)
                cv2.polylines(fr, [pts], False, (0, 0, 255))

                tup = tuple(pts[-1].astype(int).tolist())
                cv2.circle(fr, tup, 3, (0, 0, 255))


        vout.write(fr)

    vout.close()
            

if __name__=='__main__':
    import sys
    showmotion(*sys.argv[1:])
