#!/usr/bin/env python

import sys

def main(argv):
    all_people = []
    # read from stdin stream
    for line in sys.stdin:
        # split string by space-colon-space
        line = line.split(" : ")
        # convert id to int
        person = int(line[0])
        connections = line[1].strip("\n")
        connections = list(map(int, line[1].split()))
        # '%02d %s' % (person, connections)
        for connection in connections:
            print('%s\t%s' % (person, connection))

if __name__ == "__main__":
    main(sys.argv)