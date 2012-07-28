from numm import np2image
from cvframes import video_frames

def first(src, dst):
    vf = video_frames(src, height=None)
    fr = vf.next()
    np2image(fr, dst)

if __name__=='__main__':
    import sys
    first(sys.argv[1], sys.argv[2])
