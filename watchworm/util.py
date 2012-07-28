# read/write image/video

import cv2

# May require ffmpeg.
CODEC = 'MJPG'

def image2np(filepath):
    return cv2.imread(filepath)
def np2image(np, filepath):
    return cv2.imwrite(filepath, np)

# generator-based reading and writing

def VideoReader(src):
    """
for fr in VideoReader('/path/to/video.avi'):
    # do_something
"""
    vc = cv2.VideoCapture(src)
    while True:
        retval, im = vc.read()
        if retval:
            yield im# [:,:,[2,1,0]] # BGR->RGB
        else:
            raise StopIteration

class VideoWriter:
    def __init__(self, dest, fps=30):
        self.vw = cv2.VideoWriter()
        self.fps = fps
        self.dest = dest
    def write(self, fr):
        if not self.vw.isOpened():
            is_color = len(fr.shape) == 3
            if not self.vw.open(self.dest, cv2.cv.CV_FOURCC(*CODEC), self.fps, (fr.shape[1], fr.shape[0]), is_color):
                raise NodecException("The %s codec is not available" % (CODEC))

        self.vw.write(fr)

def get_fps(src):
    vc = cv2.VideoCapture(src)
    return vc.get(cv2.cv.CV_CAP_PROP_FPS)


class NodecException(Exception):
    pass
