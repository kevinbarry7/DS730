#!/usr/bin/env python

import sys

def main(argv):
    # read in stdin stream
    for i, line in enumerate(sys.stdin):
        # strip the line of whitespace
        line = line.strip()
        # split the line by tabs
        people = line.split("\t")
        # for every line after the first, begin shifting the left-most elements of the list to the end of the list (for looping purposes)
        if i != 0:
            shift_elements = people[0:i]
            people.extend(shift_elements)
            del people[0:i]
        # define the first person of the list, to whom we need to compare connections
        first_person = people[0].split()
        first_person = list(map(int, first_person))
        first_person_id = first_person[0]
        # define the first person's connections
        first_person_connections = first_person[1:]
        # create containers for who the first person might know/probably knows
        might_know = []
        probably_know = []
        # begin looping through all of the people after the first person in the stdin list
        for second_person in people[1:]:
            # convert strings to list and define these people and their connections in numeric form
            second_person = second_person.split()
            second_person = list(map(int, second_person))
            second_person_id = second_person[0]
            second_person_connections = second_person[1:]
            # set variable to keep track of how many people in the second person's list are also in the first person's list
            num_people_known = 0
            # loop through the connections of the second person
            for third_person in second_person_connections:
                # increment num_people_known if mutual acquaintences are identified between 1st/2nd people
                if third_person in first_person_connections:
                    num_people_known += 1
            # if 2nd person not a connection of the 1st person
            if second_person_id not in first_person_connections:
                # if the 2nd person has exactly 2 or 3 shared connections with the first person 
                if num_people_known in [2, 3]:
                    # then append the 2nd person's acquaitenances to the might_know list
                    might_know.append(second_person_id)
                # if the 2nd person has 4 or more shared connections with the first person
                elif num_people_known >= 4:
                    # then append the 2nd person's acquaitenances to the probably_know list
                    probably_know.append(second_person_id)
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