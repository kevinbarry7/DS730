#!/usr/bin/env python

import sys

def main(argv):
	line = sys.stdin.readline()
	line = line.split(":")
	first_person_id = int(line[0])
	first_person_connections = list(map(int, line[1].strip("\n").split(",")))
	first_person_connections_set = set(first_person_connections)
	max_people = int(first_person_connections.pop(-1))
	all_people = set(range(1, max_people +1))
	non_connections = all_people.difference(first_person_connections)
	might_know = []
	probably_know = []
	print(non_connections)

	# for line in sys.stdin:
	# 	line = line.split(":")
	# 	second_person_id = int(line[0])
	# 	second_person_connections = list(map(int, line[1].strip("\n").split(",")))
	# 	num_people_known = 0

	# 	for third_person in second_person_connections:
	# 		if third_person in first_person_connections:
	# 			num_people_known += 1

	# 		if second_person_id not in first_person_connections:
	# 			if num_people_known in [2, 3]:
	# 				might_know.append(second_person_id)

	# 			elif num_people_known >= 4:
	# 				probably_know.append(second_person_id)

	# 	# logic for printing output
	# 	if len(might_know) != 0 and len(probably_know) != 0:
	# 		might_know, probably_know = _convert_to_str(might_know, probably_know)
	# 		print('%s:Might(%s) Probably(%s)' % (first_person_id, might_know, probably_know))
		
	# 	elif len(might_know) != 0 and len(probably_know) == 0:
	# 		might_know = _convert_to_str(might_know)
	# 		print('%s:Might(%s)' % (first_person_id, might_know))
		
	# 	elif len(might_know) == 0 and len(probably_know) != 0:
	# 		probably_know = _convert_to_str(probably_know)
	# 		print('%s:Probably(%s)' % (first_person_id, probably_know))
		
	# 	else:
	# 		print('%s:' % (first_person_id))

# convert to string function
def _convert_to_str(might_know = None, probably_know = None):
	try:
		if might_know is not None and probably_know is not None:
			might_know = sorted(might_know)
			might_know = ",".join(str(value) for value in might_know)
			probably_know = sorted(probably_know)
			probably_know = ",".join(str(value) for value in probably_know)
			return(might_know, probably_know)
		
		elif might_know is not None and probably_know is None:
			might_know = sorted(might_know)
			might_know = ",".join(str(value) for value in might_know)
			return(might_know)
		
		elif might_know is None and probably_know is not None:
			probably_know = sorted(probably_know)
			probably_know = ",".join(str(value) for value in probably_know)
			return(probably_know)
	
	except Exception as error:
		return(error)

if __name__ == "__main__":
	main(sys.argv)