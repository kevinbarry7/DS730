#!/usr/bin/env python3

import sys
import math

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


def make_tree(blist):
	if len(blist) == len(buildings_list):
		blist = list(filter(lambda x: x != blist[0], blist))
		routes = []

		num_routes = math.factorial(len(blist))
		for i in range(1, num_routes+1):
			routes.append((i, []))

		num_loops = num_routes / len(blist)
		for i, route in enumerate(routes):

		added_routes = make_tree(blist)
		yield added_routes
	
	elif len(blist) < len(buildings_list) and len(blist) != 1:
		blist = list(filter(lambda x: x != blist[0], blist))


for tree in make_tree(buildings_list):
	print(tree)

# i = 0
# while i < 3:
# 	print(buildings_list)
# 	i += 1