#!/usr/bin/env python3

import sys
import math
import pprint

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


def make_tree(parent_building, blist, route = None): # [B, C, D]
	blist = list(filter(lambda x: x != parent_building, blist))
	
	for bld in blist:
		yield bld
		
		for b2 in make_tree(bld, blist):
			yield b2


master_list = []
for i, building in enumerate(buildings_list[1:]):
	ls = [building]
	num_root_parents = len(buildings_list[1:])
	total_routes = math.factorial(num_root_parents)
	routes_per_parent = total_routes/num_root_parents
	count_routes_added = 0
	i = 1

	for tree in make_tree(building, buildings_list[1:]):
		ls.append(tree)

		if len(ls) == num_root_parents:
			print("before: ", ls)
			count_routes_added += 1
			ls.append(i)
			master_list.append(ls)
			print("after: ", ls)
			i += 1

			if count_routes_added % 2 != 0:
				del ls[-2:]

			else:
				ls = [building]


pprint.pprint(master_list)
print(len(master_list))
