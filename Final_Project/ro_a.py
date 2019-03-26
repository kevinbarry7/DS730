#!/usr/bin/env python3

# 1. read in the whole file into a dict/treemap
# 2. create dict to hold optimal route info: buildings and times
# 2. lookup first element and building (key) of min time
# 	- record to optimal_route_dict
# 3. lookup building (key) from step 2, get building key of min time
# 	- record to optimal_route_dict
# 4. repeat step 3 and break after looking up first building key

import sys

buildings_dict = {}
buildings_list = []

with open(sys.argv[1],"r") as file:
	for line in file:
		line = line.split(" : ")
		building = line[0]
		travel_times = line[1].strip("\n").split(" ")
		buildings_dict[building] = list(map(int, travel_times))
		buildings_list.append(building)


for building, travel_times in buildings_dict.items():
	building_sub_dict = {}

	for i, time in enumerate(travel_times):
		building_sub_dict[buildings_list[i]] = time

	buildings_dict[building] = building_sub_dict

optimal_route_list = []

def next_optimal_building(building, final_run = False):
	travel_times = buildings_dict[building]
	if final_run is False:
		travel_times = {k: v for k, v in travel_times.items() if k not in [building, buildings_list[0]]}
		optimal_next_building = min(travel_times.items(), key=lambda x: x[1])
		optimal_route_list.append(optimal_next_building)
	else:
		first_building = buildings_list[0]
		time_to_base = travel_times[first_building]
		optimal_route_list.append((first_building, time_to_base))

num_buildings = len(buildings_list)
for i in range(0, num_buildings):
	if not optimal_route_list:
		first_building = buildings_list[i]
		# optimal_route_list.append(first_building)
		next_optimal_building(first_building)
	
	else:
		last_building_name = optimal_route_list[-1][0]
		if i < num_buildings-1:
			next_optimal_building(last_building_name)

		else:
			next_optimal_building(last_building_name, final_run = True)

route_string = buildings_list[0] + ' '
num_nodes = len(optimal_route_list) - 1
count = 0

for i, node in enumerate(optimal_route_list):
	if i != num_nodes:
		route_string = route_string + node[0] + " "
	count += node[1]

final_output = str(count) + ' ' + route_string
print(final_output)
