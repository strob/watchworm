USAGE = "python blobs.py (dump|preview) path/to/worm.avi [path/to/worm.avi [path ...]]"

import cv2
#from numm import video_frames
from cvframes import video_frames
import numpy
import os
import scipy.ndimage

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
    ENHANCE_MOTION = 1.0        # 0 is no effect, 1 is full effect
    ENHANCE_EDGES = 0.2
    BLUR = 5                    # None, or 1-N
    THRESHOLD = 65              # 0-255

    FPS = 15                    # XXX: DERIVE FROM VIDEO, OR RESAMPLE VIDEO

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

        fr2 = 255-fr
        cp2 = 255-self.comp

        fr = (fr2 - self.ENHANCE_MOTION*cp2).clip(0,255)

        if self.BLUR > 0:
            cv2.blur(fr, (self.BLUR, self.BLUR), fr)

        edges = numpy.hypot(scipy.ndimage.sobel(fr, axis=0),
                      scipy.ndimage.sobel(fr, axis=1))
        fr += self.ENHANCE_EDGES * edges.clip(0,255)

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

        self.tracker.process(contours)
        return contours

    def prune(self):
        # XXX: join & split to correct for errors, eliminate small runs, etc.

        # eliminate short-duration traces, eg. 1/2-length of max
        nFrames = numpy.array([len(X.store.keys()) for X in self.tracker.traces])
        maxLen = nFrames.max()

        out = [x[1] for x in filter(lambda x: x[0] > maxLen/2, zip(nFrames, self.tracker.traces))]

        print 'eliminated %d short-duration traces' % (len(self.tracker.traces)-len(out))
        return out

        #return self.tracker.traces

    def runBB(self, x, y, w, h):
        "return path of worm contained within bounding box"

        timings = []
        contourlist = []
        centers = []

        idx = -1

        while True:
            try:
                ofr = self.advance()
            except StopIteration:
                break

            idx += 1

            # every second
            if idx % self.FPS != 0:
                continue

            fr = self.filter(ofr)

            # crop to BB
            fr = fr[y:y+h,x:x+w]
            fr = self.threshold(fr)

            # find largest contour within BB
            contours, hierarchy = cv2.findContours(fr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            area = numpy.array([cv2.contourArea(X) for X in contours])

            print '%d contours, mean %.2f, max %d' % (len(area), area.mean(), area.max())

            contour = contours[area.argmax()].reshape((-1,2))

            # restore contour to image coordinages
            contour[:,0] += x
            contour[:,1] += y

            contourlist.append(contour)

            # cast to int or else dtype is unserializable [<numpy.int64>, <numpy.int64>]
            center = [int((contour[:,0].min() + contour[:,0].max())/2),
                      int((contour[:,1].min() + contour[:,1].max())/2)]

            centers.append(center)

            timings.append(idx/float(self.FPS))

            # adjust bounding box for next iteration
            # PADDING specifies the size of the BB at the next iteration
            PADDING = 50

            x = max(0, contour[:,0].min() - PADDING)
            w = min(ofr.shape[1], contour[:,0].max() + PADDING) - x
            
            y = max(0, contour[:,1].min() - PADDING)
            h = min(ofr.shape[0], contour[:,1].max() + PADDING) - y

            print x,y,w,h

        c_arr = numpy.array(centers)
        movements = c_arr[1:] - c_arr[:-1]
        distances= numpy.hypot(movements[:,0], movements[:,1])
        amountOfMotion = sum(distances)
        avgSpeed = amountOfMotion / (idx / float(self.FPS))

        doc = {"contourFlow": [X.tolist() for X in contourlist],
               "centerFlow": centers,
               "amountOfMotion": amountOfMotion,
               "avgSpeed": avgSpeed,
               "timings": timings}

        return doc

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
    def __init__(self, idx, payload, contour):
        self.idx = idx
        self.store = {idx:payload}
        self.contour = {idx:contour}
    def peek(self):
        return self.store[self.idx]
    def push(self, idx, payload, contour):
        self.idx = idx
        self.store[idx] = payload
        self.contour[idx] = contour
    def asarray(self):
        return numpy.array([self.store[X] for X in sorted(self.store.keys())])

class Traces(list):
    def asarray(self):
        return numpy.array([X.peek() for X in self])
    def makenew(self,idx,payload,contour):
        self.append(Trace(idx,payload,contour))

class CircleTracker:
    def __init__(self, min_a=10, dist=30, weight=[2,2,1,5]):
        self.traces = Traces()
        self.dist = dist
        self.min_a = min_a
        self.weight = numpy.array(weight)
        self.weight *= (len(self.weight) / float(self.weight.sum())) # normalize
        self.idx = 0
    def process(self, contours):
        circles = [(cv2.minEnclosingCircle(X),cv2.contourArea(X)) for X in contours]
        circles = numpy.array([[pt[0],pt[1],r,a] for (pt,r),a in circles])

        arr = self.traces.asarray()
        for idx,circle in enumerate(circles):
            if circle[3] < self.min_a:
                continue
            d_arr = None
            if len(arr) > 0:
                d_arr = abs((arr - circle)*self.weight).mean(axis=1)
            if d_arr is not None and d_arr.min() < self.dist:
                self.traces[d_arr.argmin()].push(self.idx,circle,contours[idx])
            else:
                self.traces.makenew(self.idx,circle,contours[idx])
        self.idx += 1

def preview(src):
    pipe = Pipeline(src)

    cv2.namedWindow("source")
    cv2.namedWindow("filter")
    cv2.namedWindow("threshold")

    def setThreshold(t):
        print 'set threshold', t
        pipe.THRESHOLD=t;

    def setMotion(t):
        print 'set motion', t
        pipe.ENHANCE_MOTION=t/10.0;
    def setEdges(t):
        print 'set edges', t
        pipe.ENHANCE_EDGES=t/10.0;

    def setBlur(b):
        print 'set blur', b
        pipe.BLUR=b;

    cv2.createTrackbar('threshold', 'threshold', 75, 255, setThreshold)
    cv2.createTrackbar('motion', 'filter', 10, 25, setMotion)
    cv2.createTrackbar('blur', 'filter', 5, 25, setBlur)
    cv2.createTrackbar('edges', 'filter', 2, 25, setEdges)

    while True:
        try:
            fr = pipe.advance()
        except StopIteration:
            break

        cv2.imshow("source", fr[:,:,[2,1,0]].astype(numpy.uint8)) # RGB->BGR
        fr = pipe.filter(fr)
        cv2.imshow("filter", fr)
        fr = pipe.threshold(fr)
        frview = fr.copy()      # contour is destructive
        circles = pipe.contour(fr)
        # traces = pipe.tracker.traces #pipe.prune()
        for latest in circles:
            # path = tr.asarray()[:,:2]
            # path = path.astype(numpy.int32)
            # cv2.polylines(frview, [path], False, (0,255,0))

            # latest = tr.peek()
            cv2.circle(frview, (int(latest[0]), int(latest[1])), int(latest[2]), (255,0,0))
        cv2.imshow("threshold", frview)
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
