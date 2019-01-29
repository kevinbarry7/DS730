#!/usr/bin/env python

import sys

def main(argv):
    all_pairs = {}

    for line in sys.stdin:
        line = line.strip()
        new_pair, count = line.split('\t', 1)

        if new_pair in all_pairs:
            all_pairs[new_pair] += int(count)

        else:
            all_pairs[new_pair] = int(count)


    for key, value in all_pairs.items():
        print(f"{key}\t{value}")

    all_pairs = None

# Note there are two underscores around name and main
if __name__ == "__main__":
    main(sys.argv)