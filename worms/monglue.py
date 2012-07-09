# glue between mongodb and python

import pymongo
import time
import blobs
import os
import names
import numpy
import Image
import StringIO
import base64

class Monglue:
    DATA_DIR = 'data'

    def __init__(self, server='localhost', port=3002, db='meteor'):
        self.db = pymongo.Connection(server, port)[db]
        self.worm = self.db['worm']
        self.recording = self.db['recording']

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
                    self._handleReq(doc)
                    print doc
                    
                except StopIteration:
                    time.sleep(1)
            time.sleep(1)

    def _handleReq(self, req):
        # If we were really slick, we could make a new thread, or use
        # a message queue, to handle requests. Instead, we simply
        # handle the request synchronously.

        req['unprocessed'] = False

        recording = self.db[req['recording']]

        print "GOT REQUEST !!! THE SYSTEM WORKS !!!"

        #pipeline = blobs.Pipeline(os.path.join(self.DATA_DIR, recording['filename']))

        self.request.save(req)

    def newRecording(self, filename):
        pipeline = blobs.Pipeline(os.path.join(self.DATA_DIR, filename))

        # important frames
        preview = pipeline.advance()
        comp = pipeline.comp.astype(numpy.uint8)

        doc = {"filename": filename,
               "preview": np2base64(preview),
               "comp": np2base64(comp)}

        self.recording.save(doc)        

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

    if sys.argv[1] == 'add':
        for p in sys.argv[2:]:
            m.newRecording(p)

    else:
        m.requestLoop()
