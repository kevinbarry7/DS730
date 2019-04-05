import pprint as pp
from itertools import permutations
import timeit
import math

start_time = timeit.default_timer()
def get_perm(ls, len_list, limit, count = 0, start = 0, i = 1):
	max_index = len_list-1

	if count < limit:
		ls_post = ls.copy()
		start_val = ls_post[start]
		next_val = ls_post[i]
		ls_post[start] = next_val
		ls_post[i] = start_val
		print(f"\t\t\tstart: {start} i: {i}")
		yield ls_post

		if i < max_index:
			i += 1
		else:
			if start < max_index:
				start += 1
				i = start

		if i == start and i != max_index:
			i += 1
		elif i == start and i == max_index:
			start = 0
			i = 1

		count += 1

		if count == 12:
			print("half")
		for np in get_perm(ls_post, len_list, limit, count, start, i):
			yield np

a = ['A', 'B', 'C', 'D']
# a = ['A', 'B', 'C']

perm_list = []
len_list = len(a)
f = math.factorial(len_list)

for o in get_perm(a, len_list, limit = f):
	perm_list.append(tuple(o))
	print(o)

stop_time = timeit.default_timer()

### p1

print('Time elapsed 1: ', stop_time - start_time)
p1 = set(perm_list)
print(f"{len(p1)}")

### p2

# start_time2 = timeit.default_timer()
# p2 = set(permutations(a))
# print(f"{len(p2)}")
# stop_time2 = timeit.default_timer()

# print('Time elapsed 2: ', stop_time2 - start_time2)

# print(len(p2.difference(p1)))
