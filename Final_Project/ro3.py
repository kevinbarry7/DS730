#!/usr/bin/env python3

import sys
import pprint as pp
from itertools import permutations

buildings_dict = {}
buildings_list = []

# read in file and create list of buildings and dict of buildings + times
with open(sys.argv[1],"r") as file:
	for line in file:
		line = line.split(" : ")
		building = line[0]
		travel_times = line[1].strip("\n").split(" ")
		buildings_dict[building] = list(map(int, travel_times))
		buildings_list.append(building)

# for each key, each value is a list of times. Transform each list to a dict with building + time pairs.
for building, travel_times in buildings_dict.items():
	building_sub_dict = {}

	for i, time in enumerate(travel_times):
		building_sub_dict[buildings_list[i]] = time

	buildings_dict[building] = building_sub_dict


# generator to create tree of permutations from fixed sequence
def next_node(parent_building, blist, level = None): # [B, C, D]
	blist = list(filter(lambda x: x != parent_building, blist))
	
	if level is None:
		level = 1
	
	level += 1
	
	for bld in blist:
		yield (level, bld)
	
		for b2 in next_node(bld, blist, level):
			yield b2

all_routes = []


# if next nodelevel is greater than current node level, append to current list
	# make current node level = next_node_level
# else if next node level is less than current node level, truncate list by diff

# loop through every building after building A
for i, building in enumerate(buildings_list[1:]):
	first_building = buildings_list[0]
	num_parents = len(buildings_list[1:])

	list_nodes = [building]
	parent_level = 1
	current_node_level = parent_level

	for node in next_node(building, buildings_list[1:]):
		next_node_level, building = node
		
		if next_node_level < current_node_level:
			trunc_level = (next_node_level - current_node_level) - 1
			del list_nodes[trunc_level:]

		list_nodes.append(building)
		current_node_level = next_node_level

		if len(list_nodes) == num_parents:
			all_routes.append(tuple(list_nodes))

pp.pprint(all_routes)
print(len(all_routes))

p1 = set(permutations(buildings_list[1:]))
print(len(p1))
p2 = set(all_routes)
pp.pprint(len(list(p1.difference(p2))))

# perm_tuples = list(permutations(buildings_list[1:]))
# perm_list = []
# for i in range(len(perm_tuples)):
# 	perm = list(perm_tuples[i])
# 	perm.insert(0,buildings_list[0])
# 	perm.append(buildings_list[0])
# 	perm_list.append(perm)

# pp.pprint(perm_list)


# # create new list to contain route times
# route_times = []

# # loop through every route (permutation) in all_routes and set total_time to 0
# for i, route in enumerate(all_routes):
# 	total_time = 0

# 	# loop through sequence of indices for every route and define current + next building
# 	for j in range(1, len(route)):
# 		current_building = route[j-1]
# 		next_building = route[j]

# 		# get time to go from current building to next building
# 		time_to_next_bld = buildings_dict[current_building][next_building]
# 		total_time += time_to_next_bld
	
# 	# append route index and time to route_times
# 	route_times.append((i, total_time))

# # return tuple for route of minimum travel time
# min_time = min(route_times, key = lambda route: route[1])

# # get route
# route = ' '.join(all_routes[min_time[0]])

# # subset route time
# time = min_time[1]

# print(f"{time} {route}")



# print various lists
# pp.pprint(buildings_dict)
# pp.pprint(all_routes)
# print(len(all_routes))
# pp.pprint(route_times)

