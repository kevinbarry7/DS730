#!/usr/bin/env python

import sys
import re

def main(argv):
	line = sys.stdin.readline()
	while line:
		pattern = re.compile("[a-zA-Z0-9]+")
		word_list = pattern.findall(line)
		char_counts = {}

		for word in word_list:
			for i in range(len(word)-1):
				letter = word[i]
				next_letter = word[i + 1]
				pair = letter + next_letter
				if pair in char_counts:
					char_counts[pair] += 1
				else:
					char_counts[pair] = 1

		print(char_counts)
		line = sys.stdin.readline()

#Note there are two underscores around name and main
if __name__ == "__main__":
	main(sys.argv)
