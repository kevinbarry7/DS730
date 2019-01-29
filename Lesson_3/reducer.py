#!/usr/bin/env python
#Be sure the indentation is correct and also be sure the line above this is on the first line

import sys

def main(argv):
    current_word = None
    current_count = 0
    word = None
    for line in sys.stdin:
        line = line.strip()
        word, count = line.split('\t', 1)
        count = int(count)
        if current_word == word:
            current_count += count
        else:
            if current_word:
                print('%s\t%s' % (current_word, current_count))
            current_count = count
            current_word = word
    if current_word == word:
        print('%s\t%s' % (current_word, current_count))
#Note there are two underscores around name and main if __name__ == "__main__":
if __name__ == "__main__":
    main(sys.argv)