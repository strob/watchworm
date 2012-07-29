#!/usr/bin/env python

import glob
import shutil
import os

from watchworm.first_frame import first
from watchworm.ruledcontour import contours
from watchworm.paths import path
from watchworm.showmotion import showmotion
from watchworm.jsonification import jsonify
from watchworm.makecsv import makecsv
from watchworm.circularity import circularity

INPUT = 'input'
OUTPUT= 'output'

def run():
    if not os.path.isdir(OUTPUT):
        os.makedirs(OUTPUT)
    if not os.path.isdir(INPUT):
        die('No directory named `%s` found.' % (INPUT))
    files = glob.glob('input/*.avi')
    for filename in files:
        base = os.path.basename(filename)
        outbase = os.path.join(OUTPUT, base)
        firstframe =outbase+'.first.tif' 
        if not os.path.exists(firstframe):
            first(filename, firstframe)
        contourpath =outbase+'.contours.pkl'
        if not os.path.exists(contourpath):
            contours(filename, contourpath)
        pathspath = outbase+'.path.pkl'
        if not os.path.exists(pathspath):
            path(contourpath, pathspath)
        circlespath = outbase + '.circ.tif'
        if not os.path.exists(circlespath):
            circularity(pathspath, circlespath)
        motionpath = outbase+'.motion.avi'
        if not os.path.exists(motionpath):
            showmotion(filename, 
                       pathspath,
                       motionpath)
    jsonify('input', 'output')
    makecsv()


if __name__ == '__main__':
    try:
        import argparse
    except ImportError:
        print 'argparse not found -- running anyway'
        run()
        import sys
        sys.exit(0)

        
    parser = argparse.ArgumentParser(
        description='CLI utility for watchworm')
    parser.add_argument('action', default='all', help='[all | clean]')
    args = parser.parse_args()
    
    def die(msg):
        print msg
        import sys
        sys.exit(1)
            
    if args.action == 'all':
        run()
    elif args.action == 'clean':
        shutil.rmtree('output')
    else:
        die('Action not understood.')
