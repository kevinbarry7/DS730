#!/usr/bin/env python

import sys
import re

def main(argv):
	line = sys.stdin.readline()
	while line:
		pattern = re.compile("[a-zA-Z0-9]+")
		word_list = pattern.findall(line)
		word_lengths = {}
		for word in word_list:
			word_len = len(word)
			pairs = []
			for i in range(word_len-1):
				letter = word[i]
				next_letter = word[i + 1]
				pair = letter + next_letter
				pairs.append(pair)

			if word_len in word_lengths:
				word_lengths[word_len].extend(pairs)
			else:
				word_lengths[word_len] = pairs

		for length, values in word_lengths.items():
			if length is not 1:
				most_common = max(values, key=values.count)
				print(f"{length}\t{most_common}")

		line = sys.stdin.readline()
#Note there are two underscores around name and main
if __name__ == "__main__":
	main(sys.argv)
