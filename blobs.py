import cv2
import numm
import numpy
import os

def composite(src):
    path = src + '.composite.npy'
    if os.path.exists(path):
        return numpy.load(path)
    else:
        print 'generating composite (this may take a sec ...)'
        acc = None
        for idx,fr in enumerate(numm.video_frames(uid, height=480)):
            print idx
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

        self.reader = numm.video_frames(self.src, height=480)

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
        return circles

    def continuity(self, contours):
        pass

    def prune(self):
        pass

    def run(self):
        pass



class Trace:
    def __init__(self, idx, payload):
        self._last = idx
        self.store = {idx:payload}
    def peek(self):
        return self.store[self._last]
    def push(self, idx, payload):
        self._last = idx
        self.store[idx] = payload
    def sorted(self):
        return numpy.array([self.store[X] for X in sorted(self.store.keys())])

class Traces(list):
    def asarray(self):
        return numpy.array([X.peek() for X in self])
    def makenew(self,idx,payload):
        self.append(Trace(idx,payload))

class CircleTracker:
    def __init__(self, min_r=3, dist=5):
        self.traces = Traces()
        self.dist = dist
        self.min_r = min_r
        self.idx = 0
    def process(self, circles):
        print self.idx
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


# inline numm sketch for previewing with all params
pipe = None
_offx = _offy = 0
_w = 640
_h = 480

def _make_sample_pipeline():
    global pipe
    import sys
    pipe = Pipeline(sys.argv[1])

def blit_sliver(a, fr, idx, N):
    "draw a vertical sliver, respecting mouse-pan"
    s_w = int(320/N)
    a[:,idx*s_w:(idx+1)*s_w] = fr[_offy:_offy+240,_offx+idx*s_w:_offx+(idx+1)*s_w].reshape((240,s_w,-1))

def video_out(a):
    global _w, _h
    if pipe is None:
        _make_sample_pipeline()
    else:
        try:
            fr = pipe.advance()
            _w = fr.shape[1]
            _h = fr.shape[0]
        except StopIteration:
            # loop
            _make_sample_pipeline()
            fr = pipe.advance()
        blit_sliver(a, fr, 0, 3)
        fr = pipe.filter(fr)
        blit_sliver(a, fr, 1, 3)
        fr = pipe.threshold(fr)
        blit_sliver(a, fr, 2, 3)
        circles = pipe.contour(fr)
        for c in circles:
            #print c
            if c[2] > 5:
                cv2.circle(a, (int(c[0]-_offx), int(c[1]-_offy)), int(c[2]), (255,0,0))


def mouse_in(type, px, py, button):
    global _offx, _offy
    # XXX: maybe just use OpenCV for GUI at full res (?)
    _offx = int(px*(_w-320))
    _offy = int(py*(_h-240))

if __name__=='__main__':
    # TODO: either run on- or offline analysis depending on arguments
    pass