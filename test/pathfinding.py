from watchworm.first_frame import first
from watchworm.ruledcontour import contours
from watchworm.paths import path
from watchworm.showmotion import showmotion

def testCircle(base):
    first(base, base+'.p.png')
    contours(base, base+'.c.pkl')
    path(base+'.c.pkl', base+'.p.pkl')
    showmotion(base, 
               base+'.p.pkl',
               base+'.m.avi')

if __name__=='__main__':
    testCircle('data/circleAtSpeed100.avi')
    testCircle('data/offscreenCircles100.avi')
