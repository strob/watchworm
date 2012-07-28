from numm.video import VideoWriter
from cvframes import video_frames
from numpy import zeros, uint8

def webm(src, dst):
    vf = None
    vfr = None
    for idx,fr in enumerate(video_frames(src)):
        if idx == 0:
            vf = VideoWriter(dst, fr.shape)
            vfr = zeros((fr.shape[0],fr.shape[1],3), uint8)
        # numm/py require contiguous arrays.
        vfr[:] = fr.reshape((fr.shape[0],fr.shape[1],-1))
        vf.write(vfr)
    vf.close()

if __name__=='__main__':
    import sys
    webm(sys.argv[1], sys.argv[2])
