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
	
	for i, connections in enumerate(rotate_list(all_people)):
		connections = ','.join(map(str, connections)) 
		print('%s\t%s' % (i + 1, connections))

def rotate_list(all_people):
	i = 0
	# for each person in the list
	for person in all_people:
		# roll/rotate the list leftward (minus)
		new_list = np.roll(all_people, i)
		i -= 1
		yield new_list.tolist()
		# increment rotation amount

if __name__ == "__main__":
	main(sys.argv)