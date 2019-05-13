#!/usr/bin/env python

import sys
import collections

def main(argv):
    # read in first std input
    line = sys.stdin.readline()
    first_person_connections = []
    # split the line into first person and their connections
    first_person, first_connection = _split_line(line)
    # append first connection to list
    first_person_connections.append(first_connection)
    # create container for all connections
    all_connections = []
    
    # loop through rest of standard input
    for line in sys.stdin:
        # get values for each line
        second_person, second_connection = _split_line(line)

        # if person on first line is same as person on second line, append connections
        if first_person == second_person:
            first_person_connections.append(second_connection)
        
        # else, append to total connections and reset variables for next line
        else:
            _update_total_connections(first_person, first_person_connections, all_connections)
            first_person_connections = []
            first_person = second_person
            first_person_connections.append(second_connection)

    # update total connections for final line
    _update_total_connections(first_person, first_person_connections, all_connections)
    # print(all_connections)
    
    # loop through total (all) connections, rotating the list on each iteration via generator    
    for people in _rotate_list(all_connections):
        # get first person id
        first_person_id = people[0][0]
        
        # get first person connections
        first_person_connections = people[0][1:]
        
        # set up lists to track might_know vs probably_know
        might_know = []
        probably_know = []

        # loop through second person connections
        for person in people[1:]:
            second_person_id = person[0]
            second_person_connections = person[1:]
            # set variable to keep track of how many people in the second person's list are also in the first person's list
            num_people_known = 0

            if second_person_id not in first_person_connections:
                # loop through the connections of the second person
                for connection in second_person_connections:
                    # increment num_people_known if mutual acquaintences
                    if connection in first_person_connections:
                        num_people_known += 1

                # if the 2nd person has exactly 2 or 3 shared connections with the first person, append to might_know
                if num_people_known in [2, 3]:
                    # then append the 2nd person's acquaitenances to the might_know list
                    might_know.append(second_person_id)
                
                # if the 2nd person has 4 or more shared connections with the first person
                elif num_people_known >= 4:
                    # then append the 2nd person's acquaitenances to the probably_know list
                    probably_know.append(second_person_id)

        # logic to print information
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

# function to rotate all_connections list
def _rotate_list(all_connections):
    i = 0
    # for each person in the list
    for person in all_connections:
        # creating object to rotate
        new_list = collections.deque(all_connections)
        new_list.rotate(i)
        # increment rotation amount
        i -= 1
        yield list(new_list)

# function to update all_connections list
def _update_total_connections(person, connections, all_connections):
    connections.insert(0, person)
    all_connections.append(connections)

# function to convert information before printing
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

# function to split lines
def _split_line(line):
    line = line.split("\t")
    person = int(line[0])
    connection = int(line[1])
    return(person, connection)

if __name__ == "__main__":
    main(sys.argv)