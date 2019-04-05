import pprint as pp
from itertools import permutations
import timeit

start_time = timeit.default_timer()

def get_perm(ls, len_list, start = None):
	if start is None:
		start = 0
	else:
		start += 1

	for i in range(start, len_list):
		ls_copy = ls.copy()
		start_val = ls[start]
		swap_val = ls[i]
		ls_copy[start] = swap_val
		ls_copy[i] = start_val
		yield ls_copy

		for np in get_perm(ls_copy, len_list, start):
			yield np

a = ['A', 'B', 'C']
perm_list = []
len_list = len(a)

for o in get_perm(a, len_list):
	perm_list.append(tuple(o))

p1 = set(perm_list)
print(f"{len(p1)}")

stop_time = timeit.default_timer()
print('Time elapsed 1: ', stop_time - start_time)

start_time2 = timeit.default_timer()

p2 = set(permutations(a))
print(f"{len(p2)}")

stop_time2 = timeit.default_timer()
print('Time elapsed 2: ', stop_time2 - start_time2)


# print(len(p2.difference(p1)))

