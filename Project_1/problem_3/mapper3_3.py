#!/usr/bin/env python

import sys
import numpy as np

def main(argv):
	all_people = []
	# read from stdin stream
	for line in sys.stdin:
		# split string by space-colon-space
		line = line.split(" : ")
		# convert id to int
		person = int(line[0])
		connections = line[1].strip("\n")
		# append to connections var
		# var += f"{person} {connections}\t"
		all_people.append('%s %s' % (person, connections))

	num_people = len(all_people)
	for i in range(1, num_people + 1):
		for connections in all_people:
			print('%s\t%s' % (i, connections))

if __name__ == "__main__":
	main(sys.argv)