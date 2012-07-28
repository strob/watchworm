import glob
import json
import os
import pickle
import numpy
from util import get_fps

rec = {}
allpaths = {}

def motion(path):
    dists = path[1:] - path[:-1]
    dists = numpy.hypot(*dists.T)
    return sum(dists)

if __name__=='__main__':

    for f in glob.glob('data/*.avi'):

        FPS = get_fps(f)

        base = os.path.basename(f)
        rec[base] = {"filename": os.path.basename(f)}

        paths = pickle.load(open('%s.path.pkl' % (f)))
        docs = []

        store = allpaths

        for idx,(path,smoothed) in enumerate(paths):
            arr = numpy.array(path)
            raw_motion = motion(arr[:,:2])
            # smoothed = smooth(arr)
            amnt_motion = motion(smoothed)

            distance = numpy.hypot(*(arr[0,:2] - arr[-1,:2]))

            avg_speed = FPS*amnt_motion / float(arr[-1,-1] - arr[0,-1]) # px/sec

            uid = '%s-%d' % (base, idx)
            doc = {"recording": base,
                   "center": path[0][:2],
                   "radius": path[0][2],
                   "area": path[0][3],
                   "raw_motion": raw_motion,
                   "motion": amnt_motion,
                   "distance": distance,
                   "speed": avg_speed}
            docs.append(doc)
            store[uid] = doc

        # compute recording-wide averages
        recinfo = {}

        nworms = len(paths)
        recinfo["nworms"] = nworms

        for key in ["radius", "area", "raw_motion", "motion", "distance", "speed"]:
            recinfo[key] = sum([X[key] for X in docs])/float(nworms)
            
        rec[base].update(recinfo)

    json.dump(allpaths, open("Path.json", 'w'))
    json.dump(rec, open("Recording.json", 'w'))
