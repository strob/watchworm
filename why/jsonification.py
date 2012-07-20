import glob
import json
import os
import pickle
import numpy

rec = {}
p45 = {}
p60 = {}
p50 = {}
p75 = {}

def motion(path):
    dists = path[1:] - path[:-1]
    dists = numpy.hypot(*dists.T)
    return sum(dists)

if __name__=='__main__':

    for f in glob.glob('data/*.avi'):
        base = os.path.basename(f)
        rec[base] = {"filename": os.path.basename(f)}

        for string, store in [['ADP45', p45], ['MOT60', p60], ['MBL50', p50], ['MBL75', p75]]:
            paths = pickle.load(open('%s.path%s.pkl' % (f, string)))
            docs = []
            for idx,(path,smoothed) in enumerate(paths):
                arr = numpy.array(path)
                raw_motion = motion(arr[:,:2])
                # smoothed = smooth(arr)
                amnt_motion = motion(smoothed)

                distance = numpy.hypot(*(arr[0,:2] - arr[-1,:2]))

                avg_speed = amnt_motion / float(arr[-1,-1]) # px/frame

                uid = '%s-%s-%d' % (base, string, idx)
                doc = {"recording": base,
                       "method": string,
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
            recinfo["nworms_"+string] = nworms

            for key in ["radius", "area", "raw_motion", "motion", "distance", "speed"]:
                recinfo[key+"_"+string] = sum([X[key] for X in docs])/float(nworms)
            
            rec[base].update(recinfo)
            json.dump(store, open("Path%s.json" % (string), 'w'))

    json.dump(rec, open("Recording.json", 'w'))
