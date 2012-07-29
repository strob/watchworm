import json
import csv

def makecsv():

    paths = json.load(open('Path.json'))
    writer= csv.writer(open('Path.csv', 'w'))
    keys = paths.values()[0].keys()
    keys.sort()

    writer.writerow(['id'] + keys)

    for worm,data in paths.items():
        writer.writerow([worm] + [data[x] for x in keys])


    rec = json.load(open('Recording.json'))
    writer= csv.writer(open('Recording.csv', 'w'))
    keys = rec.values()[0].keys()
    keys.sort()

    writer.writerow(['id'] + keys)

    for name,data in rec.items():
        writer.writerow([name] + [data[x] for x in keys])

if __name__=='__main__':
    makecsv()
