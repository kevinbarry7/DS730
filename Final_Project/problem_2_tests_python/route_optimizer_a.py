#!/usr/bin/env python3

import sys
import timeit

start_time = timeit.default_timer()

buildings_dict = {}
building_id_map_dict = {}

# read in file and create list of buildings and dict of buildings + times
with open(sys.argv[1],"r") as file:
	for i, line in enumerate(file):
		line = line.split(" : ")
		building = line[0]
		travel_times = line[1].strip("\n").split(" ")
		buildings_dict[i] = list(map(int, travel_times))
		building_id_map_dict[i] = building

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

# function to generate permutations recursively
def get_perm(buildings_list):
	building_list_integer = list(range(len(buildings_list)))
	building_indices = building_list_integer[1:]

	all_routes = []

	# for each building index in building indices, calculate recursion info
	for i, building in enumerate(building_indices):
		first_building = building_list_integer[0]
		num_parents = len(building_indices)

		list_nodes = [building]
		parent_level = 1
		current_node_level = parent_level

		# pass current "parent" building to generator to get all permutations
		for node in next_node(building, building_indices):
			next_node_level, building = node
			
			if next_node_level < current_node_level:
				trunc_level = (next_node_level - current_node_level) - 1
				del list_nodes[trunc_level:]

			list_nodes.append(building)
			current_node_level = next_node_level

			# this part prepends the first building to start and end of route, and append route to all_routes
			if len(list_nodes) == num_parents:
				new_list = list(list_nodes)
				new_list.insert(0, first_building)
				new_list.append(first_building)
				all_routes.append(tuple(new_list))

	return all_routes


all_routes = get_perm([i for i in building_id_map_dict.keys()])

# create new list to contain route times
route_times = []

# loop through every route (permutation) in all_routes
for i, route in enumerate(all_routes):
	total_time = 0

	# for every route, calculate travel time
	for j in range(1, len(route)):
		current_building = route[j-1]
		next_building = route[j]

		# get time to go from current building to next building
		time_to_next_bld = buildings_dict[current_building][next_building]
		
		# increment total time
		total_time += time_to_next_bld

	route_times.append((i, total_time))

# return tuple for route of minimum travel time
min_time = min(route_times, key = lambda route: route[1])

# get route
route = ' '.join([str(building_id_map_dict[i]) for i in all_routes[min_time[0]][:-1]])

# subset route time
time = min_time[1]

print(f"{time} {route}")

stop_time = timeit.default_timer()

print('Time elapsed: ', stop_time - start_time)