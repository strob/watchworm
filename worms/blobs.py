USAGE = "python blobs.py (dump|preview) path/to/worm.avi [path/to/worm.avi [path ...]]"

import cv2
#from numm import video_frames
from cvframes import video_frames
import numpy
import os

def composite(src):
    path = src + '.composite.npy'
    if os.path.exists(path):
        return numpy.load(path)
    else:
        print 'generating composite (this may take a sec ...)'
        acc = None
        for idx,fr in enumerate(video_frames(src, height=480)):
            if acc is None:
                acc = fr.astype(int)
            else:
                acc += fr
        acc /= idx
        numpy.save(path, acc)
        return acc

class Pipeline:
    # ENHANCE_MOTION = 0        # 0 is none, 1 is normal
    BLUR = 5                    # None, or 1-N
    THRESHOLD = 75              # 0-255

    def __init__(self, src):
        self.src = src

        self.comp = composite(self.src)
        self.comp = self.comp.mean(axis=2)

        self.reader = video_frames(self.src)#, height=480)

        self.tracker = CircleTracker()

    def advance(self):
        return self.reader.next()

    def filter(self, fr):
        fr = fr.mean(axis=2)
        fr = (self.comp - fr).clip(0,255)

        cv2.blur(fr, (self.BLUR, self.BLUR), fr)

        # fill dynamic range
        fr = fr-fr.min()
        if fr.max() > 0:
            fr *= (255.0/fr.max())

        fr = fr.astype(numpy.uint8)
        return fr

    def threshold(self, fr):
        fr[fr>self.THRESHOLD] = 255
        fr[fr<self.THRESHOLD] = 0
        return fr

    def contour(self, fr):
        contours, hierarchy = cv2.findContours(fr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        circles = [cv2.minEnclosingCircle(contours[idx]) for idx in range(len(contours))]
        circles = numpy.array([[pt[0],pt[1],r] for pt,r in circles])
        self.tracker.process(circles)
        return circles

    def prune(self):
        # XXX: join & split to correct for errors, eliminate small runs, etc.
        return self.tracker.traces

    def run(self):
        while True:
            try:
                fr = self.advance()
            except StopIteration:
                break
            fr = self.filter(fr)
            fr = self.threshold(fr)
            self.contour(fr)
        traces = self.prune()
        return traces


class Trace:
    def __init__(self, idx, payload):
        self.idx = idx
        self.store = {idx:payload}
    def peek(self):
        return self.store[self.idx]
    def push(self, idx, payload):
        self.idx = idx
        self.store[idx] = payload
    def asarray(self):
        return numpy.array([self.store[X] for X in sorted(self.store.keys())])

class Traces(list):
    def asarray(self):
        return numpy.array([X.peek() for X in self])
    def makenew(self,idx,payload):
        self.append(Trace(idx,payload))

class CircleTracker:
    def __init__(self, min_r=3, dist=10):
        self.traces = Traces()
        self.dist = dist
        self.min_r = min_r
        self.idx = 0
    def process(self, circles):
        arr = self.traces.asarray()
        for circle in circles:
            if circle[2] < self.min_r:
                continue
            d_arr = None
            if len(arr) > 0:
                d_arr = abs(arr - circle).mean(axis=1) # XXX: euclidian distance, r^2, etc..
            if d_arr is not None and d_arr.min() < self.dist:
                self.traces[d_arr.argmin()].push(self.idx,circle)
            else:
                self.traces.makenew(self.idx,circle)
        self.idx += 1

def preview(src):
    pipe = Pipeline(src)

    cv2.namedWindow("source")
    cv2.namedWindow("filter")
    cv2.namedWindow("threshold")

    while True:
        try:
            fr = pipe.advance()
        except StopIteration:
            break

        cv2.imshow("source", fr[:,:,[2,1,0]].astype(numpy.uint8)) # RGB->BGR
        fr = pipe.filter(fr)
        cv2.imshow("filter", fr)
        fr = pipe.threshold(fr)
        circles = pipe.contour(fr)
        traces = pipe.prune()
        for tr in traces:
            path = tr.asarray()[:,:2]
            path = path.astype(numpy.int32)
            cv2.polylines(fr, [path], False, (0,255,0))

            latest = tr.peek()
            cv2.circle(fr, (int(latest[0]), int(latest[1])), int(latest[2]), (255,0,0))
        cv2.imshow("threshold", fr)
        if cv2.waitKey(100) == 27: # escape
            break

if __name__=='__main__':
    import sys
    if sys.argv[1] == 'dump':
        import csv
        for src in sys.argv[2:]:
            path = src + '.csv'
            writer = csv.writer(open(path, 'w'))
            writer.writerow(['worm', 'frame', 'x', 'y', 'r'])

            p = Pipeline(src)
            traces = p.run()

            for t_idx,tr in enumerate(traces):
                for l_idx in sorted(tr.store.keys()):
                    pt = tr.store[l_idx]
                    writer.writerow([t_idx, l_idx, pt[0], pt[1], pt[2]])

    elif sys.argv[1] == 'preview':
        src = sys.argv[2]
        preview(src)
    else:
        print USAGE
        sys.exit(1)