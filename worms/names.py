import random

names = open("NAMES.txt").read().split("\n")

def next():
    return random.choice(names)

def jumble():
    return next().split()[0] + ' ' + next().split()[-1]
