#!/usr/bin/env python

import sys

def main(argv):
	# set initial variables
	first_vowel = None
	first_count = None
	# iterate through standard input
	for line in sys.stdin:
		# split line by colon
		line = line.split(':')
		# define first key (vowel) and value (count)
		next_vowel = line[0]
		next_count = int(line[1].strip())
		# if initial vowel and current vowel match, increment count
		if first_vowel == next_vowel:
			first_count += next_count
		else:
			# if first_vowel is not none, output key/val count
			if first_vowel is not None:
				print('%s:%s' % (first_vowel, first_count))
			# reset vars
			first_vowel = next_vowel
			first_count = next_count
	# if end of file, print results
	if next_vowel == first_vowel:
		print('%s:%s' % (first_vowel, first_count))
if __name__ == "__main__":
	main(sys.argv)