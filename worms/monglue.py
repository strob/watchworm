# glue between mongodb and python

import pymongo
from pymongo.objectid import ObjectId
import time
import blobs
import os
import names
import numpy
import Image
import StringIO
import base64
import cv2

class Monglue:
    DATA_DIR = 'data'

    def __init__(self, server='localhost', port=3002, db='meteor'):
        self.db = pymongo.Connection(server, port)[db]
        self.worm = self.db['worm']
        self.recording = self.db['recording']
        self.preview = self.db['preview']
        self.comp = self.db['comp']

        if not 'request' in self.db.collection_names():
            self.db.create_collection('request', capped=True, size=10000)
        self.request = self.db['request']
    
    def requestLoop(self):
        # double loop == double ugh: http://stackoverflow.com/questions/10321140/using-pymongo-tailable-cursors-dies-on-empty-collections
        while True: 
            cursor = self.request.find({'unprocessed': True}, tailable=True, await_data=True)
            while cursor.alive:
                try:
                    doc = cursor.next()
                    print doc
                    self._handleReq(doc)
                    
                except StopIteration:
                    time.sleep(1)
            time.sleep(1)

    def _handleReq(self, req):
        # If we were really slick, we could make a new thread, or use
        # a message queue, to handle requests. Instead, we simply
        # handle the request synchronously.

        req['unprocessed'] = False

        recording = self.recording.find_one({'_id':ObjectId(req['recording'])})
        bb = req["bb"]

        pipeline = blobs.Pipeline(os.path.join(self.DATA_DIR, recording['filename']))

        doc = pipeline.runBB(*bb)
        doc['name'] = self.generateName()
        doc['bb'] = bb
        doc['recording'] = req['recording']
        doc['contour'] = doc['contourFlow'][0]

        self.worm.insert(doc)

        req['trackingOk'] = True

        self.request.update({"_id": req["_id"]}, {"unprocessed": False})


    def newRecording(self, filename):
        pipeline = blobs.Pipeline(os.path.join(self.DATA_DIR, filename))

        # important frames
        preview = pipeline.advance()
        comp = pipeline.comp.astype(numpy.uint8)

        # remove extension
        name = '.'.join(filename.split('.')[:-1])

        doc = {"filename": filename,
               "name": name}

        _id = self.recording.save(doc)
        print filename, _id

        self.preview.save({"recording": _id,
                           "preview": np2base64(preview)})
        self.comp.save({"recording": _id,
                        "comp": np2base64(comp)})
        
        doc["_id"] = _id
        return doc

    def analyzeRecording(self, rec):
        pipeline = blobs.Pipeline(os.path.join(self.DATA_DIR, rec['filename']))
        traces = pipeline.run()
        for worm in traces:

            bb = cv2.boundingRect(worm.contour[min(worm.contour.keys())])

            c_arr = worm.asarray()[:,:2]
            movements = c_arr[1:] - c_arr[:-1]
            distances= numpy.hypot(movements[:,0], movements[:,1])
            amountOfMotion = sum(distances)
            avgSpeed = amountOfMotion / (pipeline.idx / float(pipeline.FPS))
            doc = {'recording': rec['_id'],
                   'name': self.generateName(),
                   'amountOfMotion': amountOfMotion,
                   'avgSpeed': avgSpeed,
                   'bb': bb}
            print doc['name']
            self.worm.insert(doc)
            
            # 'circleFlow': worm.asarray().astype(int).tolist()}

    def generateName(self):
        name = None
        while name is None or self.worm.find_one({"name":name}) is not None:
            if self.worm.count() >= len(names.names):
                name = names.jumble()
            else:
                name = names.next()
        return name

def np2base64(np):
    im = Image.fromarray(np)
    sin = StringIO.StringIO()
    sout = StringIO.StringIO()
    im.save(sin, format='png')
    sin.seek(0)
    base64.encode(sin, sout)
    sout.seek(0)
    return "data:image/png;base64,"+sout.read()

if __name__=='__main__':
    import sys

    m = Monglue()

    if len(sys.argv) > 1 and sys.argv[1] == 'add':
        for p in sys.argv[2:]:
            rec = m.newRecording(p)
            m.analyzeRecording(rec)

    else:
        m.requestLoop()
