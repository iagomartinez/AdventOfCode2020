import sys
import unittest
import time
from datetime import datetime

class Tests(unittest.TestCase):
    def test_part2(self):
        _, busids = parse('../_data/day13_sample.txt')
        buses = [(ix, int(bus)) for ix, bus in enumerate(busids) if bus != 'x']
        offset,maxid = max(buses, key=second)
        acc = 1        
        timestamp = buses[0][1]
        t0 = time.perf_counter()
        while True:
            tmp = [((timestamp + b[0]) % b[1] == 0) for b in buses]
            if all(tmp):
                print(f'candidate timestamp found: {timestamp}')
                break
            timestamp += buses[0][1]
            t1 = time.perf_counter()

        print(f'timestamp {timestamp} found in {t1 - t0:0.4f} seconds')
        self.assertEqual(1068781, timestamp)

def second(tup):
    return tup[1]

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