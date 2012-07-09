# glue between mongodb and python

import pymongo
import time
import blobs
import os
import names

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

        #pipeline = blobs.Pipeline(os.path.join(DATA_DIR, recording['filename']))

        self.request.save(req)

    def generateName(self):
        name = None
        while name is None or self.worm.find_one({"name":name}) is not None:
            if self.worm.count() >= len(names.names):
                name = names.jumble()
            else:
                name = names.next()
        return name

if __name__=='__main__':
    m = Monglue()
    m.requestLoop()
