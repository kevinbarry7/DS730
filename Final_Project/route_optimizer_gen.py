#!/usr/bin/env python3

import timeit
import sys

start_time = timeit.default_timer()

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


# Transform each list to a dict with building + time pairs.
for building, travel_times in buildings_dict.items():
	building_sub_dict = {}

	for i, time in enumerate(travel_times):
		building_sub_dict[buildings_list[i]] = time

	buildings_dict[building] = building_sub_dict

# generator to create tree of permutations
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

# create tuples of generated nodes
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
			new_list = list(list_nodes)
			new_list.insert(0, first_building)
			new_list.append(first_building)
			all_routes.append(tuple(new_list))


route_times = []

# loop through every permutation and get time
for i, route in enumerate(all_routes):
	total_time = 0

	for j in range(1, len(route)):
		current_building = route[j-1]
		next_building = route[j]

		time_to_next_bld = buildings_dict[current_building][next_building]
		total_time += time_to_next_bld
	
	route_times.append((i, total_time))

# return tuple for route of minimum travel time
min_time = min(route_times, key = lambda route: route[1])

# get route
route = ' '.join(all_routes[min_time[0]][:-1])

# subset route time
time = min_time[1]

print(f"{time} {route}")

stop_time = timeit.default_timer()

print('Time elapsed: ', stop_time - start_time) 