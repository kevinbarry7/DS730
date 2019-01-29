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
			char_count = []
			for i in range(word_len-1):
				letter = word[i]
				next_letter = word[i + 1]
				pair = letter + next_letter
				char_count.append([pair, 1])

			if word_len in word_lengths:
				word_lengths[word_len].extend(char_count)
			else:
				word_lengths[word_len] = char_count

		for length, values in word_lengths.items():
			most_common = max(values, key=values.count)
			most_common = most_common[0]
			print(f"{length}\t{most_common}")

		line = sys.stdin.readline()
#Note there are two underscores around name and main
if __name__ == "__main__":
	main(sys.argv)
