import sys
import unittest
from datetime import datetime

def extractminutes(tup):
    _, times = tup
    return times % 1

def main():
    print('----------- day13 -----------')
    file='../_data/day13.txt'
    with open(file, 'r', newline='', encoding='utf-8') as f:
        timestamp = int(f.readline().strip())
        busids = f.readline().strip()

    schedule = [int(id) for id in busids.split(',') if id != 'x']

    # for each bus, find out how many times they have run since time 0
    timesrun = [(id, timestamp / id) for id in schedule]
    # order by greatest partial run (i.e. next one to complete)
    timesrun.sort(key=extractminutes, reverse=True)
    id, runs =timesrun[0]
    # find out the last timestamp that bus ran
    lastrun = timestamp - id * int(runs)
    # et voilá:
    print(f'Next bus: {id}, result: {id * (id - lastrun)}')    

if __name__ == '__main__':
    sys.exit(main())