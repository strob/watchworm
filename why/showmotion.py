from cvframes import video_frames, get_fps
from numm.video import VideoWriter
import numpy
import cv2
import pickle
from jsonification import motion # this should be elsewhere ...
from ruledcontour import getRule # "" ""

def showmotion(orig, src, paths, dest):
    FPS = get_fps(orig)

    paths = pickle.load(open(paths))

    CROP = getRule('crop', orig)

    # divide by number of frames
    # px/second
    avg_speeds = [FPS*motion(y)/paths[idx][-1][0][-1] for idx,(x,y) in enumerate(paths)]
    avg_speed = sum(avg_speeds) / len(avg_speeds)

    vout = None
    fr = None
    orig_vout = None
    orig_fr = None

    orig_vf = video_frames(orig, height=None);

    for idx,ofr in enumerate(video_frames(src, height=None)):
        orig_ofr = orig_vf.next()
        if CROP > 0:
            orig_ofr = orig_ofr[CROP:-CROP,CROP:-CROP]

        if idx == 0:
            vout = VideoWriter(dest, ofr.shape)
            fr = numpy.zeros(ofr.shape, dtype=numpy.uint8)
            orig_vout = VideoWriter(dest.replace('showmotion', 'origmotion'), orig_ofr.shape, {"fps": FPS})
            orig_fr = numpy.zeros(orig_ofr.shape, dtype=numpy.uint8)


        fr[:] = 255-ofr             # contiguity ...
        orig_fr[:] = orig_ofr

        for vo, f in [[orig_vout, orig_fr], [vout, fr]]:

            speeds = []

            for p_idx,(raw,smooth) in enumerate(paths):
                raw = filter(lambda x: x[4] <= idx, raw)
                smooth = smooth[:max(0,len(raw)-5)]

                raw = numpy.array(raw)
                pts = raw[:,:2].astype(numpy.int32)
                cv2.polylines(f, [pts], False, (255, 0, 0))

                tup = tuple(raw[-1,:2].astype(int).tolist())
                cv2.circle(f, tup, raw[-1,2].astype(int), (255, 0, 0))
                cv2.circle(f, tup, 3, (255, 0, 0))

                speed = 0
                if len(pts) > 1:
                    speed = numpy.hypot(*(pts[-1] - pts[-2]).T)
                speeds.append(speed)
                txt = "%.2f (%.2f)" % (avg_speeds[p_idx], speed)
                cv2.putText(f, txt, tup, cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0))

                # & smoothed
                if len(smooth) > 0:
                    pts = numpy.array(smooth).astype(numpy.int32)
                    cv2.polylines(f, [pts], False, (0, 0, 255))

                    tup = tuple(pts[-1].astype(int).tolist())
                    cv2.circle(f, tup, 3, (0, 0, 255))

            txt = "%.2f (%.2f), N=%d" % (avg_speed, sum(speeds)/len(speeds), len(paths))
            cv2.putText(f, txt, (30,30), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255))

            vo.write(f)

    vout.close()
    orig_vout.close()
            

if __name__=='__main__':
    import sys
    showmotion(*sys.argv[1:])
