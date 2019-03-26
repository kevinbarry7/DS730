#!/usr/bin/env python3

# 0. create list to contain routes
# 1. get building list minus first building
# 2. begin looping through building list and add first blding to sublist.
# 3. get building list minus first building again
# 4. begin looping through building list and add first building to sublist.

import sys
from itertools import permutations

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


perm = permutations(buildings_list[1:])
l = len(list(perm))
print(l)
# for i in perm:
# 	print(i)