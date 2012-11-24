import cv2
import json
import numpy as np
import os

RULES = json.load(open('RULES.json'))
def getRule(key, src):
    return RULES.get(os.path.basename(src), RULES["default"]).get(key, RULES["default"][key])
def setRule(key, src, val):
    RULES.setdefault(os.path.basename(src), {})[key] = val
    json.dump(RULES, open('RULES.json', 'w'))

if __name__=='__main__':
    import sys
    for path in sys.argv[1:]:
        reader = cv2.VideoCapture(path)

        THRESH = getRule("threshold", path)

        def onChange(newval):
            global THRESH
            THRESH = newval

        cv2.namedWindow("changethreshold", 1)
        cv2.createTrackbar("Threshold", "changethreshold", getRule("threshold", path), 255, onChange)

        while cv2.waitKey(50) != 10: # enter
            (succ, fr) = reader.read()
            if not succ:
                # finished playing video
                break
            fr = 255*(fr>THRESH).astype(np.uint8)
            # fr = cv2.resize(fr, (640,480))
            cv2.imshow("thresholdme", fr)
        
        setRule("threshold", path, THRESH)
