import cv2

# simulate numm-like video reader iteration

def get_fps(src):
    vc = cv2.VideoCapture(src)
    return vc.get(cv2.cv.CV_CAP_PROP_FPS)

def video_frames(src, **kw):
    vc = cv2.VideoCapture(src)
    while True:
        retval, im = vc.read()
        if retval:
            yield im[:,:,[2,1,0]] # BGR->RGB
        else:
            raise StopIteration
