#!/usr/bin/env python

import sys
import re

def main(argv):
	line = sys.stdin.readline()
	while line:
		pattern = re.compile("[a-zA-Z0-9]+")
		word_list = pattern.findall(line)
		for word in word_list:
			word_len = len(word)
			for i in range(word_len-1):
				letter = word[i]
				next_letter = word[i + 1]
				pair = letter + next_letter
				print(f"{word_len}\t{pair}")
		line = sys.stdin.readline()
#Note there are two underscores around name and main
if __name__ == "__main__":
	main(sys.argv)
