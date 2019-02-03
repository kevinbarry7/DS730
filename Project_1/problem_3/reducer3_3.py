#!/usr/bin/env python

import sys

def main(argv):
	# read in stdin stream
	line = sys.stdin.readline()
	first_person_index, first_person_id, first_person_connections = _get_row_values(line)
	# create containers for who the first person might know/probably knows
	might_know = []
	probably_know = []
		
	# begin looping through all of the people after the first person in the stdin list
	for second_line in sys.stdin:
		second_person_index, second_person_id, second_person_connections = _get_row_values(second_line)
		# print(second_person_index, second_person_id, second_person_connections)
		
		if first_person_index == second_person_index:
			# set variable to keep track of how many people in the second person's list are also in the first person's list
			num_people_known = 0

			if second_person_id not in first_person_connections:
				# loop through the connections of the second person
				for connection in second_person_connections:
					# increment num_people_known if mutual acquaintences are identified between 1st/2nd people
					if connection in first_person_connections:
						num_people_known += 1
			
				# if the 2nd person has exactly 2 or 3 shared connections with the first person 
				if num_people_known in [2, 3]:
					# then append the 2nd person's acquaitenances to the might_know list
					might_know.append(second_person_id)
				
				# if the 2nd person has 4 or more shared connections with the first person
				elif num_people_known >= 4:
					# then append the 2nd person's acquaitenances to the probably_know list
					probably_know.append(second_person_id)

		else:
			# logic for printing output
			if len(might_know) != 0 and len(probably_know) != 0:
				might_know, probably_know = _convert_to_str(might_know, probably_know)
				print('%s:Might(%s) Probably(%s)' % (first_person_id, might_know, probably_know))
			
			elif len(might_know) != 0 and len(probably_know) == 0:
				might_know = _convert_to_str(might_know)
				print('%s:Might(%s)' % (first_person_id, might_know))
			
			elif len(might_know) == 0 and len(probably_know) != 0:
				probably_know = _convert_to_str(probably_know)
				print('%s:Probably(%s)' % (first_person_id, probably_know))
			
			else:
				print('%s:' % (first_person_id))

			first_person_index = second_person_index
			first_person_id = second_person_id
			first_person_connections = second_person_connections
			probably_know = []
			might_know = []

def _get_row_values(line):
	# strip the line of whitespace
	line = line.strip()
	# split the line by tabs
	people = line.split("\t")	
	# define the first person of the list, to whom we need to compare connections
	person_index = int(people[0])
	# define the first person's connections
	value = list(map(int, people[1].split()))
	first_person_id = value[0]
	first_person_connections = value[1:]
	return(person_index, first_person_id, first_person_connections)

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