#!/usr/bin/env python

import sys

def main(argv):
    var = ''
    # set final count to get N count of total people
    final_count = 0
    # read from stdin stream
    for line in sys.stdin:
        # split string by space-colon-space
        line = line.split(" : ")
        # convert id to int
        person = int(line[0])
        connections = line[1].strip("\n")
        # append to connections var
        # var += f"{person} {connections}\t"
        var += '%s\t%s' % (person, connections)
        # increment final count
        final_count += 1
    # replicate connections list N (final_count) times
    for i in range(0, final_count):
        print(var)
if __name__ == "__main__":
    main(sys.argv)