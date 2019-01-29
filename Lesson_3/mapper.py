#!/usr/bin/env python
#Be sure the indentation is identical and also be sure the line above this is on the first line

import sys
import re

def main(argv):
    line = sys.stdin.readline()
    pattern = re.compile("[a-zA-Z0-9]+")
    while line:
        for word in pattern.findall(line):
            print(word+"\t"+"1")
        line = sys.stdin.readline()
#Note there are two underscores around name and main if __name__ == "__main__":
if __name__ == "__main__":
    main(sys.argv)