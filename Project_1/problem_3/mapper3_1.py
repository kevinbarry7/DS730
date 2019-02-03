#!/usr/bin/env python

import sys

def main(argv):
	for line in sys.stdin:
		line = line.split(" : ")
		person = int(line[0])
		connections = line[1].strip("\n")
		connections = list(map(int, connections.split(" ")))
		non_connections = []

		for next_line in sys.stdin:
			next_line = next_line.split(" : ")
			next_person = int(next_line[0])
			next_person_connections = next_line[1].strip("\n")
			next_person_connections = list(map(int, next_person_connections.split(" ")))
			next_person_connections_formatted = _convert_to_str(next_person_connections)		
			print('%s:%s' % (next_person, next_person_connections_formatted))

			for connection in next_person_connections:
				if connection not in connections:
					non_connections.append(connection)

		connections = _convert_to_str(connections)
		max_connections = max(set(non_connections))
		print('%s:%s,%s' % (person, connections, max_connections))

def _convert_to_str(some_list):
	some_list = sorted(some_list)
	some_list = ",".join(str(value) for value in some_list)
	return(some_list)
			
if __name__ == "__main__":
	main(sys.argv)