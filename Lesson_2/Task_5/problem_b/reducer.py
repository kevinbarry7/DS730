#!/usr/bin/env python

import sys

def main(argv):
    prev_word_length = None
    pairs_list = []

    for line in sys.stdin:
        line = line.strip()
        curr_word_len, pair = line.split('\t', 1)

        if prev_word_length is None:
            pairs_list.append(pair)
            prev_word_length = curr_word_len

        elif curr_word_len == prev_word_length:
            pairs_list.append(pair)

        else:
            print_stdout(pairs_list, prev_word_length)

            if prev_word_length != curr_word_len:
                pairs_list = []
                prev_word_length = curr_word_len
                pairs_list.append(pair)

    print_stdout(pairs_list, prev_word_length)

def print_stdout(pairs_list, prev_word_length):
    most_common = max(pairs_list, key=pairs_list.count)
    print(f"{prev_word_length}\t{most_common}")

# Note there are two underscores around name and main
if __name__ == "__main__":
    main(sys.argv)