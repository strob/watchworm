from watchworm.first_frame import first
from watchworm.ruledcontour import contours
from watchworm.paths import path
from watchworm.showmotion import showmotion

def testCircle(base):
    first(base, base+'.path.png')
    contours(base, base+'.contour.pkl')
    path(base+'.contour.pkl', base+'.path.pkl')
    showmotion(base, 
               base+'.path.pkl',
               base+'.motion.avi')

if __name__=='__main__':
    testCircle('data/circleAtSpeed100.avi')
    testCircle('data/offscreenCircles100.avi')
