import sys
import unittest
from datetime import datetime

def extractwholeminutes(tup):
    _, minutes = tup
    return minutes % 1

def part1(schedule, timestamp):
    # for each bus, find out how many times they have run since time 0
    timesrun = [(id, timestamp / id) for id in schedule]
    # order by greatest partial run (i.e. next one to complete)
    timesrun.sort(key=extractwholeminutes, reverse=True)
    print(timesrun)
    id, runs =timesrun[0]
    # find out the last timestamp that bus ran
    lastrun = timestamp - id * int(runs)
    # et voilá:
    print(f'Next bus: {id}, result: {id * (id - lastrun)}')

def parse(file):
    with open(file, 'r', newline='', encoding='utf-8') as f:
        timestamp = int(f.readline().strip())
        busids = f.readline().strip().split(',')
    return timestamp, busids

def main():
    print('----------- day13 -----------')
    file='../_data/day13.txt'
    timestamp, busids = parse(file)

    schedule = [int(id) for id in busids if id != 'x']
    part1(schedule, timestamp)

if __name__ == '__main__':
    sys.exit(main())