import glob
import json
import os
import pickle
import numpy

rec = {}
p45 = {}
p60 = {}

# XXX: A lot of analysis seems to be happening here!

SMOOTHING_WINDOW_LEN = 10
def smooth(path):
    window = numpy.kaiser(SMOOTHING_WINDOW_LEN, 4)
    window = window / window.sum()
    y = numpy.convolve(path[:,0], window, mode='valid')
    x = numpy.convolve(path[:,1], window, mode='valid')
    return numpy.array([y,x]).T

def motion(path):
    # should be smoothed
    dists = path[1:] - path[:-1]
    dists = numpy.hypot(*dists.T)
    return sum(dists)

if __name__=='__main__':

    for f in glob.glob('data/*.avi'):
        base = os.path.basename(f)
        rec[base] = {"filename": os.path.basename(f)}

        for string, store in [['ADP45', p45], ['MOT60', p60]]:
            paths = pickle.load(open('%s.path%s.pkl' % (f, string)))
            for idx,path in enumerate(paths):
                arr = numpy.array(path)
                raw_motion = motion(arr[:,:2])
                smoothed = smooth(arr)
                amnt_motion = motion(smoothed)

                distance = numpy.hypot(*(arr[0,:2] - arr[-1,:2]))

                avg_speed = amnt_motion / float(arr[-1,-1]) # px/frame

                uid = '%s-%s-%d' % (base, string, idx)
                doc = {"recording": base,
                       "center": path[0][:2],
                       "radius": path[0][2],
                       "area": path[0][3],
                       "raw_motion": raw_motion,
                       "motion": amnt_motion,
                       "distance": distance,
                       "speed": avg_speed}
                store[uid] = doc


    json.dump(p45, open("PathADP45.json", 'w'))
    json.dump(p60, open("PathMOT60.json", 'w'))
    json.dump(rec, open("Recording.json", 'w'))
