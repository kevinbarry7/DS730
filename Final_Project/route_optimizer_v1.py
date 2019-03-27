#!/usr/bin/env python3

import sys
import pprint as pp
from itertools import permutations

buildings_dict = {}
building_id_map_list = []
building_id_map_dict = {}

# read in file and create list of buildings and dict of buildings + times
with open(sys.argv[1],"r") as file:
	for i, line in enumerate(file):
		line = line.split(" : ")
		building = line[0]
		travel_times = line[1].strip("\n").split(" ")
		buildings_dict[i] = list(map(int, travel_times))
		building_id_map_list.append((i, building))
		building_id_map_dict[i] = building

# generate permutations of routes
perm_list = list(permutations([i for i, name in building_id_map_list[1:]]))
all_routes = []
for i in range(len(perm_list)):
	perm = list(perm_list[i])
	perm.insert(0,building_id_map_list[0][0])
	perm.append(building_id_map_list[0][0])
	all_routes.append(perm)

# create new list to contain route times
route_times = []

# loop through every route (permutation) in all_routes and set total_time to 0
for i, route in enumerate(all_routes):
	total_time = 0

	# loop through sequence of indices for every route and define current + next building
	for j in range(1, len(route)):
		current_building = route[j-1]
		next_building = route[j]

		# get time to go from current building to next building
		time_to_next_bld = buildings_dict[current_building][next_building]
		total_time += time_to_next_bld
	
	# append route index and time to route_times
	route_times.append((i, total_time))


# get minimum travel time
min_time = min(route_times, key = lambda route: route[1])

# get route
route = ' '.join([str(building_id_map_dict[i]) for i in all_routes[min_time[0]][:-1]])

# subset route time
time = min_time[1]

print(f"{time} {route}")
