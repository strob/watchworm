import glob
import pickle
import numpy as np

def distance(path):
    path = np.array(path)
    return np.hypot(*(path[0,:2] - path[-1,:2]))

def angles(path):
    "angles between each point and the next"
    path = np.array(path)
    dists = path[1:,:2] - path[:-1,:2]
    return np.arctan2(*dists.T)

def circularity(path):
    "total amount of rotation: sum of magnitude of differential angles."
    a = angles(path)
    d_a = a[1:] - a[:-1]
    return sum(abs(d_a))

def relativeCircularity(paths):
    "circularity per length-of-worm traveled."
    c = circularity(paths[1])
    return c / relativeMotion(paths)

def motion(path):
    path = np.array(path)
    dists = path[1:,:2] - path[:-1,:2]
    dists = np.hypot(*dists.T)
    return sum(dists)

def area(rawpath):
    rawpath = np.array(rawpath)
    return rawpath[:,3].mean()

def diameter(rawpath):
    rawpath = np.array(rawpath)
    return 2*rawpath[:,2].mean()

def relativeMotion(paths):
    "% of length"
    raw = paths[0]
    smooth = paths[1]
    amnt_motion = motion(smooth)
    return amnt_motion / diameter(raw)

def time(rawpath, fps):
    # TODO: incorporate framerate into path pickle.
    return (rawpath[-1][4] - rawpath[0][4]) / float(fps)

def speed(paths, fps):
    "px / sec"
    raw = paths[0]
    smooth = paths[1]
    amnt_motion = motion(smooth)
    return amnt_motion / time(raw, fps)

def relativeSpeed(paths, fps):
    "% / sec"
    return relativeMotion(paths) / time(paths[0], fps)
