import glob
import json
import os

rec = {}
for f in glob.glob('data/*.avi'):
    rec[os.path.basename(f)] = {"filename": os.path.basename(f)}

json.dump(rec, open("Recording.json", 'w'))
