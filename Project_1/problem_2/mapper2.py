#!/usr/bin/env python

import sys

def main(argv):
    # define lowercase and uppercase vowels
    lower_vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    upper_vowels = map(lambda v: v.upper(), lower_vowels)
    # combine lower & upper case vowels into one list
    vowels = list(zip(lower_vowels, upper_vowels))
    for line in sys.stdin:
        # split the line into a list at any occurrence white space
        line = line.split()
        # loop through every word in a line
        for word in line:
            # and keep track of vowels present for every word
            vowels_present = ''
            # loop through list of vowels
            for lower_vowel, upper_vowel in vowels:
                # for every occurrence of a vowel, add to our list of vowels_present
                if lower_vowel in word:
                    vowels_present += lower_vowel * word.count(lower_vowel)
                if upper_vowel in word:
                    vowels_present += upper_vowel * word.count(upper_vowel)
            # print present vowels
            print('%s:%s' % (vowels_present, 1))
if __name__ == "__main__":
    main(sys.argv)