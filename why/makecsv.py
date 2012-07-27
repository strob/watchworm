import json
import csv

paths = json.load(open('Path.json'))
writer= csv.writer(open('Path.csv', 'w'))
keys = ['recording', 'motion', 'radius', 'center', 'area', 'raw_motion', 'speed', 'distance']

writer.writerow(['id'] + keys)

for worm,data in paths.items():
    writer.writerow([worm] + [data[x] for x in keys])
