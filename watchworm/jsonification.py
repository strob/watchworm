import glob
import json
import os
import pickle
import numpy
from util import get_fps
from quantification import *

rec = {}
allpaths = {}

def jsonify(inputdir, outputdir):
    for f in glob.glob(os.path.join(inputdir, '*.avi')):
        outbase = os.path.join(outputdir, os.path.basename(f))

        FPS = get_fps(f)

        base = os.path.basename(f)
        rec[base] = {"filename": os.path.basename(f)}

        paths = pickle.load(open('%s.path.pkl' % (outbase)))
        docs = []

        store = allpaths

        for idx,(path,smoothed) in enumerate(paths):
            uid = '%s-%d' % (base, idx)
            doc = {"recording": base,
                   "center (x,y)": path[0][:2],
                   "radius (px)": diameter(path)/2,
                   "area (px)": area(path),
                   "raw_motion (px)": motion(path),
                   "motion (px)": motion(smoothed),
                   "distance (px)": distance(path),
                   "speed (px/sec)": speed([path,smoothed], FPS),
                   "rel_motion (% of length)": relativeMotion([path,smoothed]),
                   "rel_speed (%/sec)": relativeSpeed([path,smoothed], FPS),
                   "circularity (radians)": circularity(smoothed),
                   "rel_circularity (radians/%-of-length)": relativeCircularity([path,smoothed])
               }
            docs.append(doc)
            store[uid] = doc

        # compute recording-wide averages
        recinfo = {}

        nworms = len(paths)
        recinfo["nworms"] = nworms

        keys = docs[0].keys()
        keys.remove("recording")
        keys.remove("center (x,y)")
        for key in keys:
            recinfo[key] = sum([X[key] for X in docs])/float(nworms)
            recinfo["std_dev:"+key] = np.std([X[key] for X in docs])

        rec[base].update(recinfo)

    json.dump(allpaths, open("Path.json", 'w'))
    json.dump(rec, open("Recording.json", 'w'))

if __name__=='__main__':
    jsonify('data')
