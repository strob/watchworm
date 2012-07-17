from numpy import uint8
from numm import np2image
from cvframes import video_frames

def composite(src, dst):
    acc = None
    for idx,fr in enumerate(video_frames(src, height=None)):
        if acc is None:
            acc = fr.astype(int)
        else:
            acc += fr
    acc /= idx
    np2image(acc.astype(uint8), dst)

if __name__=='__main__':
    import sys
    composite(sys.argv[1], sys.argv[2])
