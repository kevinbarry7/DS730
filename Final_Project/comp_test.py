#!/usr/bin/env python3

import timeit
import sys

from itertools import permutations

buildings_list = ['A','B','C','D','E','F','H','I','J']

start_time = timeit.default_timer()

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

stop_time = timeit.default_timer()
print('Time elapsed: ', stop_time - start_time) 

print(len(list(all_routes)))

start_time2 = timeit.default_timer()

p2 = permutations(buildings_list[1:])

stop_time2 = timeit.default_timer()

l = len(list(p2))
print(l)

print('Time elapsed: ', stop_time2 - start_time2) 





