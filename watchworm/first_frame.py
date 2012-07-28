from util import VideoReader, np2image

def first(src, dst):
    vf = VideoReader(src)
    fr = vf.next()
    np2image(fr, dst)

if __name__=='__main__':
    import sys
    first(sys.argv[1], sys.argv[2])
