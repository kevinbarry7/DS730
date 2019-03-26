#!/usr/bin/env python3

# 0. create list to contain routes
# 1. get building list minus first building
# 2. begin looping through building list and add first blding to sublist.
# 3. get building list minus first building again
# 4. begin looping through building list and add first building to sublist.

import sys
import itertools

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
		yield f"1: {bld}"
		for b2 in make_tree(bld, blist):
			yield f"2: {b2}"

for i, building in enumerate(buildings_list[1:]):
	print("BUILDING ", building)
	for tree in make_tree(building, buildings_list[1:]):
		print(tree)